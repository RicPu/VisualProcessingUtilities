import os
import subprocess


def _process_video(input_path, output_path, frame_rate, crf, preset):
    """This function internally uses ffmpeg to interpolate frames in the
        input video, encode it with libx264 codec, and save it to the
        specified output path.
    """

    command = [
        'ffmpeg', '-i', str(input_path),
        '-vf', f'minterpolate=fps={frame_rate}',
        '-c:v', 'libx264', '-crf', str(crf),
        '-preset', preset, str(output_path)
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, check=True)


def interpolate(
        input_folder, output_folder=None, frame_rate=32,
        crf=17, preset='veryslow'):
    """Video interpolation using ffmpeg.

    Args:
        input_folder (str): The path to the folder containing input videos.
        output_folder (str, optional): The path to the folder where processed
            videos will be saved. If not provided, a folder named 'output'
            will be created in the current working directory. Defaults to
            None.
        frame_rate (int, optional): The desired frame rate of the output
            videos. Defaults to 32.
        crf (int, optional): Constant Rate Factor for video compression.
            A lower value results in better quality but larger file sizes.
            Defaults to 18.
        preset (str, optional): Preset for x264 encoder.
            A slower preset provides better compression and quality.
            Defaults to 'veryslow'.
    """

    if output_folder is None:
        output_folder = os.path.join(os.getcwd(), 'output')
    
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        if os.path.isfile(input_path):
            try:
                _process_video(input_path, output_path,
                               frame_rate, crf, preset)
            except subprocess.CalledProcessError as e:
                print(f"Error processing video {input_path}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
