#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re

import numpy as np
from PIL import Image

def reverse(filename:str, save="full"):
    """
    Reverse a heatmap

    @param filename: png heatmap to reverse
    @param save: Determines way of saving. 'full' saves to matrix. 'cols' saves as (x,y,rgb) pairs
    """
    im = Image.open(filename)

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
