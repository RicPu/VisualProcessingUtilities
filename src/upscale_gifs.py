import os
import cv2
import subprocess

from super_image import DrlnModel, ImageLoader
from PIL import Image


def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Cannot open {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return int(fps)


def to_frames(gif_path, output_dir='frames'):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'frame_%04d.png')
    command = f'ffmpeg -i {gif_path} {output_path}'
    subprocess.run(command, check=True)


def to_gif(frame_rate):
    command = f'ffmpeg -framerate {frame_rate} -i scaled/frame_04%d.png -vf "fps={frame_rate}" output.gif'
    subprocess.run(command, check=True)


def upscale(scale=2):
    model = DrlnModel.from_pretrained('eugenesiow/drln-bam', scale=scale)
    os.makedirs('./scaled', exist_ok=True)

    images = os.listdir('frames')
    for image in images:
        image_path = os.path.join('frames', image)
        image = Image.open(image_path)
        preds = model(ImageLoader.load_image(image))
        ImageLoader.save_image(preds, f'./scaled/frame_%04d.png')


if __name__ == '__main__':
    print(get_fps("kitten.gif"))