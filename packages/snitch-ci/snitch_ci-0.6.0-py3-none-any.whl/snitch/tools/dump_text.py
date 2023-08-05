#!/usr/bin/python3
"""
Takes a PNG image as parameter and prints the OCR result to the standard output.
"""
import os
import sys

from PIL import Image
import cv2
import pytesseract

from snitch.ocr import ocr, DEFAULT_SCALE_FACTOR, DEFAULT_INTERPOLATION


def test_methods(img_path, factor=DEFAULT_SCALE_FACTOR, interpolation=DEFAULT_INTERPOLATION, lang='eng'):
    # Read image using opencv
    img = cv2.imread(img_path)
    # Extract the file name without the file extension
    file_name = os.path.basename(os.path.splitext(img_path)[0]+'_x{}'.format(factor))
    # Create a directory for outputs
    output_path = os.path.join(os.path.dirname(img_path), file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Rescale the image, if needed.
    img = cv2.resize(img, None, fx=factor, fy=factor, interpolation=interpolation)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise (not useful here)
    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.erode(img, kernel, iterations=2)
    #img = cv2.dilate(img, kernel, iterations=1)

    # Apply threshold to get image with only black and white
    # pylint: disable=line-too-long
    images = {
        ('threshold', 'gaussian', '9', 'binary')     : cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'gaussian', '7', 'binary')     : cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'gaussian', '5', 'binary')     : cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'gaussian', '3', 'binary')     : cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'none',     '0', 'binary')     : cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'gaussian', '9', 'tozero')     : cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'gaussian', '7', 'tozero')     : cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'gaussian', '5', 'tozero')     : cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'gaussian', '3', 'tozero')     : cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'none',     '0', 'tozero')     : cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'gaussian', '9', 'binary_otsu'): cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '7', 'binary_otsu'): cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '5', 'binary_otsu'): cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '3', 'binary_otsu'): cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'none',     '0', 'binary_otsu'): cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '9', 'tozero_otsu'): cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '7', 'tozero_otsu'): cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '5', 'tozero_otsu'): cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'gaussian', '3', 'tozero_otsu'): cv2.threshold(cv2.GaussianBlur(img, (3, 3), 0), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'none',     '0', 'tozero_otsu'): cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('adaptive',  'gaussian', '9', 'binary_otsu'): cv2.adaptiveThreshold(cv2.GaussianBlur(img, (9, 9), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'gaussian', '7', 'binary')     : cv2.adaptiveThreshold(cv2.GaussianBlur(img, (7, 7), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'gaussian', '5', 'binary')     : cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'gaussian', '3', 'binary')     : cv2.adaptiveThreshold(cv2.GaussianBlur(img, (3, 3), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'none',     '0', 'binary')     : cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('threshold', 'median',   '9', 'binary')     : cv2.threshold(cv2.medianBlur(img, 9), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'median',   '7', 'binary')     : cv2.threshold(cv2.medianBlur(img, 7), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'median',   '5', 'binary')     : cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'median',   '3', 'binary')     : cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'none',     '0', 'binary')     : cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1],
        ('threshold', 'median',   '9', 'tozero')     : cv2.threshold(cv2.medianBlur(img, 9), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'median',   '7', 'tozero')     : cv2.threshold(cv2.medianBlur(img, 7), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'median',   '5', 'tozero')     : cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'median',   '3', 'tozero')     : cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'none',     '0', 'tozero')     : cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO)[1],
        ('threshold', 'median',   '9', 'binary_otsu'): cv2.threshold(cv2.medianBlur(img, 9), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '7', 'binary_otsu'): cv2.threshold(cv2.medianBlur(img, 7), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '5', 'binary_otsu'): cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '3', 'binary_otsu'): cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'none',     '0', 'binary_otsu'): cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '9', 'tozero_otsu'): cv2.threshold(cv2.medianBlur(img, 9), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '7', 'tozero_otsu'): cv2.threshold(cv2.medianBlur(img, 7), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '5', 'tozero_otsu'): cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'median',   '3', 'tozero_otsu'): cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('threshold', 'none',     '0', 'tozero_otsu'): cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1],
        ('adaptive',  'median',   '9', 'binary_otsu'): cv2.adaptiveThreshold(cv2.medianBlur(img, 9), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'median',   '7', 'binary')     : cv2.adaptiveThreshold(cv2.medianBlur(img, 7), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'median',   '5', 'binary')     : cv2.adaptiveThreshold(cv2.medianBlur(img, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'median',   '3', 'binary')     : cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        ('adaptive',  'none',     '0', 'binary')     : cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
    }

    # for each threshold method, save the preprocessed image and the ocr’ed text
    for key, img in images.items():
        # Save the filtered image in the output directory
        options_str = '{}_{}'.format(file_name, '_'.join(key))
        save_path = os.path.join(output_path, options_str)

        result = ocr(img, imgoutput=save_path+'png', txtoutput=save_path+'txt')

        print('{} {} //'. format('/'*42, options_str))
        print(result)


def main():
    if len(sys.argv) < 2:
        print("Missing required parameter")
        sys.exit(1)

    image = sys.argv[1]
    #for i in range(1, 5):
    #    test_methods(image, factor=i)
    test_methods(image, 2, interpolation=cv2.INTER_CUBIC, lang='eng+equ')


if __name__ == '__main__':
    main()
