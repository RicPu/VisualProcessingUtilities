# Visual-Processing-Utilities

## Tools

### Smart Cropping
This Python script provides a function to crop images and remove surrounding white borders. It's particularly useful for preprocessing images taken as screenshots.

**Usage**

``` python
from smart_cropping import crop_image

cropped_image = crop_image('input_image_path.png', 'output_image_path.png')
```

![Example Image](assets/smart_cropping.png)

### Interpolation with FFmpeg
This Python script provides functionality to interpolate videos using FFmpeg, a powerful multimedia processing tool. This script is particularly useful when you have a folder of videos to interpolate all in the same manner. Simply specify the input folder containing your videos and the output folder where the processed videos will be saved, and the script will take care of the rest. Adjust the parameters (frame_rate, crf, preset) according to your specific requirements for video interpolation. Ensure FFmpeg is properly installed and accessible for the script to function correctly.

**Functionality**
1. **_process_video**: Internal function to process a single video file using FFmpeg. It interpolates frames to achieve the desired frame rate and compresses the video using the specified CRF and preset.
2. **interpolate**: Main function to interpolate all videos in the input folder. It iterates through each video file, processes it using _process_video, and saves the processed video in the output folder.

**Usage**

``` python
from video_interpolation import interpolate

interpolate('input_videos', 'output_videos', frame_rate=32, crf=18, preset='slow')
```

## Requirements

Make sure the following dependencies are installed:
- **FFmpeg**: Ensure FFmpeg is installed on your system and accessible in the PATH.
- **Python Libraries**: The following Python libraries are required:
    - NumPy
    - OpenCV
    - Matplotlib

    These can be installed via pip:

    ``` python
    pip install numpy opencv-python matplotlib
    ```
