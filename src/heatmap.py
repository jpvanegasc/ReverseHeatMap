#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re

import numpy as np
from PIL import Image

def __get_scale(filename:str, high, low):
    """
    Generate scaling coefficients between a given scale and the real life values.

    @param filename: png of heatmap scale
    @param high: real life value of the heatmap at the top of the scale file
    @param low: real life value of the heatmap at the bottom of the scale file

    Usage: Provide a png file whose top and bottom values are known. The file is 'filename', and 
    'high' and 'low' are the real values.

    Important: The gradient must be in the negative y direction. (The scale gets darker as it goes to the 
    bottom of the screen)
    """
    im = Image.open(filename)

    size = im.size
    x_max = size[0]
    y_max = size[1]

    im_high_px = im.getpixel((0,0))
    im_low_px = im.getpixel((x_max-1,y_max-1))

    im_high = im_high_px[0] + im_high_px[1] + im_high_px[2]
    im_low = im_low_px[0] + im_low_px[1] + im_low_px[2]

    intensity_diff = im_high - im_low
    real_diff = high - low

    return (real_diff, intensity_diff, low)


def __scaled_intensity(x, real, image, low):
    """
    Change from rgb intensity to scaled values
    """
    factor = (x-low)*real/image
    return (factor + low)


def reverse(filename:str, save="full", scale_data={}):
    """
    Reverse a heatmap. If scale_data is provided, the intensity is scaled accordingly.

    @param filename: png heatmap to reverse
    @param save: Determines way of saving. 'full' saves to matrix. 'cols' saves as (x,y,I) pairs
    @param scale_data: Dict with scale filename, and real life high and low values
    """
    im = Image.open(filename)

    if bool(scale_data):
        try:
            r_d, i_d, l = __get_scale(scale_data["filename"], scale_data["high"], scale_data["low"])
        except KeyError:
            raise KeyError("Invalid scale_data dict. Keys must be 'filename', 'high' and 'low'.")

        scale = lambda x: __scaled_intensity(x, r_d, i_d, l)
    else:
        scale = lambda x: x

    size = im.size
    x_max = size[0]
    y_max = size[1]

    print(f"Image is {x_max} by {y_max} pixels")

    pixels = []
    x = 0
    y = 0

    while (x < x_max):
        while (y < y_max):
            pixels.append([x, y, im.getpixel((x,y))])
            y += 1

        x += 1
        y = 0

    rev = []

    pattern = re.compile(r"\D")

    for each in pixels:
        x = each[0]
        y = each[1]
        rgb = str(each[2]).split(",")

        r = pattern.sub('', rgb[0])
        g = pattern.sub('', rgb[1])
        b = pattern.sub('', rgb[2])

        rev.append([x,y,r,g,b])

    rev = sorted(rev)

    filename_clean = filename.replace('.png', '')

    if save == "full":
        heat = np.zeros((x_max, y_max))
    elif save == "cols":
        file = open(f"{filename_clean}_reversed.csv",'w+')
        file.write("x,y,rgb_total\r\n")
    else:
        raise ValueError("Invalid save arg.")

    x_temp = 0
    for each in rev:
        total = int(each[2]) + int(each[3]) + int(each[4])
        total = scale(total)

        string = str(each[0]) + ',' + str(each[1]) + ',' + str(total) + '\n'

        if save == "full":
            heat[each[0], each[1]] = total
        elif save == "cols":
            file.write(string)

            if each[0] == x_temp:
                file.write(string)
            else:
                file.write('\n')
                file.write(string)
                x_temp = each[0]

    if save == "full":
        with open(f"{filename_clean}_reversed.csv", 'w+') as f:
            for x in range(x_max):
                for y in range(y_max):
                    f.write(str(heat[x][y]) + ',')
                f.write('\n')
    elif save == "cols":
        file.close()
