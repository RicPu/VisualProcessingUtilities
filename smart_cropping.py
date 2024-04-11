import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


class NoBordersDetectedError(Exception):

    def suggest_resolution(self):
        return 'Consider adjusting the threshold parameter to a lower value. \
            The default background color is 255 (white).'


def _find_border(gray_image, direction, non_white_pixels):
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

    if not os.path.isfile(img_path):
        raise FileNotFoundError(f'The file {img_path} does not exist.')

    if output_path is not None and not os.path.isdir(os.path.dirname(output_path)):
        raise FileNotFoundError(f'The directory {os.path.dirname(output_path)} does not exist.')

    if not isinstance(margin, int) or margin < 0:
        raise ValueError('Margin must be a non-negative integer.')


def _get_non_white_pixels(gray_image, threshold=255):

    return np.where(gray_image < threshold)


def _calculate_borders(gray_image, non_white_pixels):

    borders = {}
    directions = ['left', 'right', 'top', 'bottom']
    for direction in directions:
        borders[direction] = _find_border(gray_image, direction, non_white_pixels)
    return borders


def _crop_and_visualize(image, borders, margin, output_path):

    x_left, _ = borders['left']
    x_right, _ = borders['right']
    _, y_top = borders['top']
    _, y_bottom = borders['bottom']

    x_left = max(0, x_left - margin)
    x_right = min(image.shape[1] - 1, x_right + margin)
    y_top = max(0, y_top - margin)
    y_bottom = min(image.shape[0] - 1, y_bottom + margin)

    padded_image = np.ones((y_bottom - y_top + 2 * margin, x_right - x_left + 2 * margin, 3), dtype=np.uint8) * 255
    padded_image[margin:-margin, margin:-margin] = image[y_top:y_bottom, x_left:x_right]

    output_path = output_path or 'output_images/cropped_image.jpg'
    output_path = output_path if '' in output_path else output_path
    cv2.imwrite(output_path, padded_image)

    _visualize_images(image, borders, padded_image)

    return padded_image


def crop_image(img_path, output_path=None, margin=10):

    try:
        _validate_input(img_path, output_path, margin)

        image = cv2.imread(img_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        non_white_pixels = _get_non_white_pixels(gray_image)
        borders = _calculate_borders(gray_image, non_white_pixels)

        if all(borders.values()):
            return _crop_and_visualize(image, borders, margin, output_path)
        else:
            raise NoBordersDetectedError('No borders were detected in the image.')
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
