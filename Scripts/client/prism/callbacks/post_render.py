import os


def __init__(core, plugin):
    core.registerCallback("postRender", postRender, plugin=plugin)


# Handle the output result after rendering
def postRender(**kwargs):
    global state
    state = kwargs.get("state", None)

    identifier = state.l_taskName.text()
    if state.gb_slack.isChecked():
        if state.chb_slackPublish.isChecked():
            outputPath = kwargs.get("settings", None)["outputName"]

            seq, shot, identifier, version = self.getVersionInfo(
                outputPath, mode="render"
            )

            ext = os.path.splitext(outputPath)[1].replace(".", "")

            rangeType = state.cb_rangeType.currentText()

            if rangeType == "Single Frame" or rangeType in ["Scene", "Shot"]:
                startFrame = state.l_rangeStart.text()
                endFrame = state.l_rangeEnd.text()

            if rangeType == "Custom":
                startFrame = state.sp_rangeStart.text()
                endFrame = state.sp_rangeEnd.text()

            if rangeType == "Expression":
                self.core.popup(
                    "Your render has been published but the Slack plugin does not support expression ranges yet."
                )
                return

            if ext in ["exr", "png", "jpg"]:
                if rangeType == "Single Frame":
                    outputList = [outputPath]

                if rangeType != "Single Frame" and startFrame == endFrame:
                    file = outputPath.replace(
                        "#" * self.core.framePadding, str(startFrame)
                    )
                    outputList = [file]

                if rangeType != "Single Frame" and startFrame < endFrame:
                    if state.chb_mediaConversion.isChecked() is False:
                        convert = self.convert_image_sequence(self.core, outputPath)
                        outputList = [convert]
                    else:
                        option = state.cb_mediaConversion.currentText().lower()
                        ext = self.retrieveExtension(option)

                        base = os.path.basename(outputPath).split(".")[0]
                        version_directory = os.path.dirname(os.path.dirname(outputPath))
                        aov_directory = os.path.basename(os.path.dirname(outputPath))
                        file = base.split(f"_{aov_directory}")[0]

                        converted_directory = (
                            f"{version_directory} ({ext})/{aov_directory}"
                        )
                        converted_files = f"{converted_directory}/{file} ({ext})_{aov_directory}.{ext}"

                        outputList = [converted_files]

                        if ext in ["png", "jpg"]:
                            framePad = "#" * self.core.framePadding
                            sequence = f"{converted_directory}/{file} ({ext})_{aov_directory}.{framePad}.{ext}"
                            convert = self.convert_image_sequence(self.core, sequence)
                            outputList = [convert]

            self.publish_to_slack(outputList, seq, shot, identifier, version, mode="SM")
    return
