import os
import cv2
import subprocess
from matplotlib import pyplot as plt

def process_video(input_path: str, output_path: str, frame_rate=32, crf=18, preset='veryslow'):

    cap = cv2.VideoCapture(input_path)
    ret, frame = cap.read()
    cap.release()

    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title(f"{os.path.basename(input_path)}")
    plt.axis('off')
    plt.xticks([]), plt.yticks([])
    plt.show()

    command = f'ffmpeg -i "{input_path}" -vf "minterpolate=fps={frame_rate}" -c:v libx264 -crf {crf} -preset {preset} "{output_path}"'
    subprocess.run(command, stdout=subprocess.DEVNULL, shell=True, check=True)

def interpolate_videos(input_folder, output_folder, frame_rate=32, crf=18, preset='veryslow'):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        if os.path.isfile(input_path):
            process_video(input_path, output_path, frame_rate, crf, preset)