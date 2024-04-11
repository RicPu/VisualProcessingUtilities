import os
import subprocess


def _process_video(input_path, output_path, frame_rate, crf, preset):
    try:
        command = [
            'ffmpeg', '-i', str(input_path),
            '-vf', f'minterpolate=fps={frame_rate}',
            '-c:v', 'libx264', '-crf', str(crf),
            '-preset', preset, str(output_path)
        ]
        subprocess.run(
            command, stdout=subprocess.DEVNULL,
            shell=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error processing video {input_path}: {e}")


def interpolate_videos(
        input_folder, output_folder, frame_rate=32,
        crf=18, preset='veryslow'):
    """Video interpolation using ffmpeg.

    Args:
        input_folder (str): The path to the folder containing input videos.
        output_folder (str): The path to the folder where processed videos
            will be saved.
        frame_rate (int, optional): The desired frame rate of the output
            videos. Defaults to 32.
        crf (int, optional): Constant Rate Factor for video compression.
            A lower value results in better quality but larger file sizes.
            Defaults to 18.
        preset (str, optional): Preset for x264 encoder.
            A slower preset provides better compression and quality.
            Defaults to 'veryslow'.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        if os.path.isfile(input_path):
            try:
                _process_video(
                    input_path, output_path,
                    frame_rate, crf, preset
            )
            except Exception as e:
                print(f"Error processing video {input_path}: {e}")
