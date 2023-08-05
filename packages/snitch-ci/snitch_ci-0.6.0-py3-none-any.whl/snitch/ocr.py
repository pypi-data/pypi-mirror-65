#!/usr/bin/python3
"""
Takes a PNG image as parameter and prints the OCR result to the standard output.
"""

import logging as log

import numpy as np
import pytesseract
import cv2

DEFAULT_SCALE_FACTOR = 2
DEFAULT_INTERPOLATION = cv2.INTER_CUBIC


def ocr(image, imgoutput=None, txtoutput=None, lang='eng', character_subset=''):
    """
    :param image: the cv2 image object to perform OCR on (output of cv2.imread)
    :param imgoutput: the filename to save the image (default doesn’t save file)
    :param txtoutput: the filename to save the ocr’ed text (default doesn’t save file)
    :param character_subset: a string containing the characters to
    :return: the output text
    """
    if imgoutput:
        cv2.imwrite(imgoutput, image)
    cfg = ''
    if character_subset:
        cfg = "-c tessedit_char_whitelist='{}'".format(character_subset)

    text = pytesseract.image_to_string(image, lang=lang, config=cfg)

    if txtoutput:
        with open(txtoutput, 'w', encoding='utf-8') as f:
            f.write(text)

    return text


def process_image(image, factor=DEFAULT_SCALE_FACTOR, interpolation=DEFAULT_INTERPOLATION, lang='eng', character_subset=''):
    """
    :param image: the image to use as input, or a string of the path to the image
    :param factor: the scale factor: 2 means an image 2 times bigger
    :param interpolation: the interpolation method to use when scaling the image
    :param lang: the expected language (as a 3 letter code) of the recognized text,
        multiple language can be specified using ’+’ as delimiter
    :return: the output text
    """
    # Read image using opencv
    if isinstance(image, np.ndarray):
        img = image
    elif isinstance(image, str):
        img = cv2.imread(image)
    else:
        raise TypeError('«{}» is not a supported image type.'.format(type(image)))

    # Rescale the image, if needed.
    img = cv2.resize(img, None, fx=factor, fy=factor, interpolation=interpolation)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise (not useful here)
    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.erode(img, kernel, iterations=2)
    #img = cv2.dilate(img, kernel, iterations=1)

    # Apply threshold to get image with only black and white
    img = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1]

    result = ocr(img, lang=lang, character_subset=character_subset)

    log.info('Image recognition result\n%s\n', result)
    return result
