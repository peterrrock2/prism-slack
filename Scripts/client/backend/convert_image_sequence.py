import os
import subprocess
import glob
import re

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


# Convert an image sequence to a video
@err_catcher(name=__name__)
def convert_image_sequence(core, sequence):
    folder_path = os.path.dirname(sequence)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the "slack" output folder
    input_sequence = convert_sequence_path(core, sequence)

    # Determine the starting frame
    start_frame = determine_start_frame(input_sequence)

    # Construct input and output paths
    output_file = construct_output_file(input_sequence)

    # Run ffmpeg to create the video
    output_file = convert_to_mp4(core, input_sequence, start_frame, output_file)

    return output_file


# Convert the sequence path to a more universal format
def convert_sequence_path(core, sequence):
    if core.appPlugin.pluginName == "Houdini":
        input_sequence = sequence.replace(".$F4.", ".%04d.")
    else:
        input_sequence = sequence.replace(".####.", ".%04d.")

    return input_sequence


# Construct the output file path for ffmpeg
def construct_output_file(input_sequence):
    basename = os.path.basename(input_sequence).split(".%04d.")[0]
    output_file = os.path.join(basename + ".mp4")

    return output_file


# Determine the starting frame of the sequence
def determine_start_frame(core, input_sequence):
    # Search for matching files to determine the start frame
    pattern = input_sequence.replace(".%04d.", ".*.")
    files = sorted(glob.glob(pattern))
    if not files:
        core.popup(f"No files found matching pattern: {pattern}")
        return

    start_frame = re.search(r"\.(\d{4})\.", files[0])
    if start_frame:
        start_frame = start_frame.group(1)
    else:
        core.popup("Failed to determine the starting frame.")
        return


# Convert the image sequence to an mp4 video
def convert_to_mp4(core, input_sequence, start_frame, output_file):
    ffmpegPath = os.path.join(core.prismLibs, "Tools", "FFmpeg", "bin", "ffmpeg.exe")
    ffmpegPath = ffmpegPath.replace("\\", "/")

    if not os.path.exists(ffmpegPath):
        print(f"ffmpeg not found at {ffmpegPath}")
        return

    try:
        result = subprocess.run(
            [
                ffmpegPath,
                "-framerate",
                "24",
                "-start_number",
                start_frame,
                "-i",
                input_sequence,
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                output_file,
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg: {e.stderr.decode()}")
        return

    output_file = output_file.replace("\\", "/")

    return output_file


# Get proper extension from media conversion type
def retrieve_extension(option):
    if "png" in option:
        ext = "png"
    elif "jpg" in option:
        ext = "jpg"
    elif "mp4" in option:
        ext = "mp4"
    elif "mov" in option:
        ext = "mov"
    else:
        ext = option

    return ext


def handle_media_conversion_checkbox(state, core, ext, outputPath):
    option = state.cb_mediaConversion.currentText().lower()

    base = os.path.basename(outputPath).split(".")[0]
    top_directory = os.path.dirname(outputPath)

    converted_directory = f"{top_directory} ({ext})"
    converted_file = f"{converted_directory}/{base} ({ext}).{ext}"
    outputList = [converted_file]

    if option in ["png", "jpg"]:
        framePad = "#" * core.framePadding
        sequence = f"{converted_directory}/{base} ({ext}).{framePad}.{ext}"
        convert = convert_image_sequence(sequence)
        outputList = [convert]
    return outputList


def handle_single_frame(outputPath):
    return [outputPath]


def handle_scene_shot(state, core, outputPath):
    startFrame = state.l_rangeStart.text()
    endFrame = state.l_rangeEnd.text()

    if startFrame == endFrame:
        file = outputPath.replace("#" * core.framePadding, str(startFrame))
        outputList = [file]

    elif startFrame < endFrame:
        convert = convert_image_sequence(outputPath)
        outputList = [convert]

    else:
        raise ValueError("Invalid range.")

    return outputList


def handle_custom(state, core, outputPath):
    startFrame = state.sp_rangeStart.text()
    endFrame = state.sp_rangeEnd.text()

    if startFrame == endFrame:
        file = outputPath.replace("#" * core.framePadding, str(startFrame))
        outputList = [file]

    elif startFrame < endFrame:
        convert = convert_image_sequence(outputPath)
        outputList = [convert]

    else:
        raise ValueError("Invalid range.")

    return outputList


def convert_png_jpg_to_outputList(state, core, ext, outputPath):
    rangeType = state.cb_rangeType.currentText()

    if rangeType == "Expression":
        core.popup(
            "Your render has been published but the Slack plugin does not support expression ranges yet."
        )
        raise ValueError("Invalid range type.")

    if state.chb_mediaConversion.isChecked():
        return handle_media_conversion_checkbox(outputPath, ext)

    if rangeType == "Single Frame":
        return handle_single_frame(outputPath)

    if rangeType in ["Scene", "Shot"]:
        return handle_scene_shot(outputPath)

    elif rangeType == "Custom":
        return handle_custom(outputPath)
    else:
        raise ValueError("Invalid range type.")
