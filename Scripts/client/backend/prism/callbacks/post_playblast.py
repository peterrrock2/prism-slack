import os


def __init__(core, plugin):
    core.registerCallback("postPlayblast", postPlayblast, plugin=plugin)


# Handle output result after playblast
def postPlayblast(**kwargs):
    state = kwargs.get("state", None)

    identifier = state.l_taskName.text()
    if state.gb_slack.isChecked():
        if state.chb_slackPublish.isChecked():
            outputPath = kwargs.get("outputpath", None)

            seq, shot, identifier, version = get_version_info(outputPath, mode="pb")

            ext = os.path.splitext(outputPath)[1].replace(".", "")

            rangeType = state.cb_rangeType.currentText()
            core.popup(
                f"Seq: {seq}, \nShot: {shot}, \nIdentifier: {identifier}, \nVersion: {version}, \nExt: {ext}, \nRangeType: {rangeType}"
            )
            if rangeType == "Single Frame" or rangeType in ["Scene", "Shot"]:
                startFrame = state.l_rangeStart.text()
                endFrame = state.l_rangeEnd.text()

            if rangeType == "Custom":
                startFrame = state.sp_rangeStart.text()
                endFrame = state.sp_rangeEnd.text()

            if rangeType == "Expression":
                core.popup(
                    "Your render has been published but the Slack plugin does not support expression ranges yet."
                )
                return

            if ext in ["png", "jpg"]:
                if rangeType == "Single Frame":
                    outputList = [outputPath]

                if rangeType != "Single Frame" and startFrame == endFrame:
                    file = outputPath.replace("#" * core.framePadding, str(startFrame))
                    outputList = [file]

                if rangeType != "Single Frame" and startFrame < endFrame:
                    if state.chb_mediaConversion.isChecked() is False:
                        convert = convert_image_sequence(core, outputPath)
                        outputList = [convert]

                if state.chb_mediaConversion.isChecked() is True:
                    option = state.cb_mediaConversion.currentText().lower()

                    base = os.path.basename(outputPath).split(".")[0]
                    top_directory = os.path.dirname(outputPath)

                    converted_directory = f"{top_directory} ({ext})"
                    converted_file = f"{converted_directory}/{base} ({ext}).{ext}"
                    outputList = [converted_file]

                    if option in ["png", "jpg"]:
                        framePad = "#" * core.framePadding
                        sequence = (
                            f"{converted_directory}/{base} ({ext}).{framePad}.{ext}"
                        )
                        convert = convert_image_sequence(core, sequence)
                        outputList = [convert]
            core.popup(outputList)
            publish_to_slack(outputList, seq, shot, identifier, version, mode="SM")

    return
