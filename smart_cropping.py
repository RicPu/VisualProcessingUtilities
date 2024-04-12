import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


class NoBordersDetectedError(Exception):

    def suggest_resolution(self):
        return 'Consider adjusting the threshold parameter to a lower value. \
            The default background color is 255 (white).'


def _find_border(gray_image, direction, non_white_pixels):
    """ Find the border coordinates in the specified direction.

    This function finds the border coordinates in the specified direction based
    on the non-white pixels' coordinates.
    """

    if direction == 'left':
        x, y = (non_white_pixels[1].min(),
                non_white_pixels[0][non_white_pixels[1].argmin()])
    elif direction == 'right':
        x, y = (non_white_pixels[1].max(),
                non_white_pixels[0][non_white_pixels[1].argmax()])
    elif direction == 'top':
        x, y = (non_white_pixels[1][non_white_pixels[0].argmin()],
                non_white_pixels[0].min())
    elif direction == 'bottom':
        x, y = (non_white_pixels[1][non_white_pixels[0].argmax()],
                non_white_pixels[0].max())
    else:
        return None
    return x, y


def _visualize_images(original_image, detected_borders, cropped_image):
    """ Visualize the detected borders and the cropped image.

    This function plots two subplots:
    - The first subplot shows the original image with detected borders
        highlighted in red.
    - The second subplot shows the cropped image.
    """

    try:
        plt.subplot(1, 2, 1)
        plt.imshow(original_image[..., ::-1])
        plt.plot([detected_borders['left'][0], detected_borders['right'][0],
                  detected_borders['right'][0], detected_borders['left'][0],
                  detected_borders['left'][0]],
                 [detected_borders['top'][1], detected_borders['top'][1],
                  detected_borders['bottom'][1], detected_borders['bottom'][1],
                  detected_borders['top'][1]], 
                 color='red')
        plt.title('Detected Borders')

        plt.subplot(1, 2, 2)
        plt.imshow(cropped_image[..., ::-1])
        plt.title('Cropped Image')

        plt.show()
    except Exception as e:
        print(f'Error during visualization: {e}')


def _validate_input(img_path, output_path, margin):
    """ Validate the input parameters for the crop_image function.

    This function checks if the input image file exists, if the output
    directory exists (if provided), and if the margin parameter is a
    non-negative integer.
    """

    if not os.path.isfile(img_path):
        raise FileNotFoundError(f'The file {img_path} does not exist.')

    if (output_path is not None and
        not os.path.isdir(os.path.dirname(output_path))):
        raise FileNotFoundError('The directory does not exist.')

    if not isinstance(margin, int) or margin < 0:
        raise ValueError('Margin must be a non-negative integer.')


def _get_non_white_pixels(gray_image, threshold):

    return np.where(gray_image < threshold)


def _calculate_borders(gray_image, non_white_pixels):
    """ Calculate the borders of non-white regions in the image.

    This function determines the borders of non-white regions in the provided
    grayscale image. It iterates through each direction (left, right, top,
    bottom) and finds the corresponding border.
    """

    borders = {}
    directions = ['left', 'right', 'top', 'bottom']
    for direction in directions:
        borders[direction] = _find_border(
            gray_image, direction, non_white_pixels
        )
    return borders


def _crop_and_visualize(image, borders, margin, output_path):
    """ Crop the image based on detected borders, add a margin, and visualize
            the result.

    This function crops the input image based on the detected borders and adds
    a margin around the cropped region. It then visualizes the original image
    with detected borders and the cropped image.
    """

    x_left, _ = borders['left']
    x_right, _ = borders['right']
    _, y_top = borders['top']
    _, y_bottom = borders['bottom']

    x_left = max(0, x_left - margin)
    x_right = min(image.shape[1] - 1, x_right + margin)
    y_top = max(0, y_top - margin)
    y_bottom = min(image.shape[0] - 1, y_bottom + margin)

    padded_image = np.ones((
        y_bottom - y_top + 2 * margin,
        x_right - x_left + 2 * margin, 3),
        dtype=np.uint8) * 255
    
    padded_image[margin:-margin, margin:-margin] = image[
        y_top:y_bottom, x_left:x_right
    ]

    output_path = output_path or 'output_images/cropped_image.jpg'
    output_path = output_path if '' in output_path else output_path
    cv2.imwrite(output_path, padded_image)

    _visualize_images(image, borders, padded_image)

    return padded_image


def crop_image(img_path, output_path=None, margin=10, threshold=255):
    """ Crop an image to remove surrounding white borders.

    Args:
        img_path (str): The path to the input image file.
        output_path (str, optional): The path to save the cropped image.
            If not provided, the cropped image will not be saved.
        margin (int, optional): The margin size (in pixels) to preserve around
            the cropped image. Defaults to 10.
        threshold (int, optional): The threshold value for considering pixels
            as non-white. Pixels with values above this threshold will be
            considered non-white. Defaults to 255.

    Raises:
        NoBordersDetectedError: Raised when no borders are detected in
            the image.
        FileNotFoundError: Raised when the input image file is not found.
        ValueError: Raised when invalid input parameters are provided.
        Exception: Raised for any other unexpected errors during the cropping
            process.

    Returns:
        numpy.ndarray or None: If successful, returns the cropped image as a
            NumPy array. If an error occurs, returns None.
    """

    try:
        _validate_input(img_path, output_path, margin)

        image = cv2.imread(img_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        non_white_pixels = _get_non_white_pixels(gray_image, threshold)
        borders = _calculate_borders(gray_image, non_white_pixels)

        if all(borders.values()):
            return _crop_and_visualize(image, borders, margin, output_path)
        else:
            raise NoBordersDetectedError(
                'No borders were detected in the image.'
            )
    except NoBordersDetectedError as e:
        print(f'Error: {e}')
        print(f'Suggested resolution: {e.suggest_resolution()}')
        return None
    except (FileNotFoundError, ValueError) as e:
        print(f'Error: {e}')
        return None
    except Exception as e:
        print(f'Error during cropping: {e}')
        return None
