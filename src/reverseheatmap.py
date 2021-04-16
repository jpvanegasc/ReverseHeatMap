#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re

from PIL import Image

# open the image and determine size.
im = Image.open("heatmap.png")

size = im.size
x_max = size[0]
y_max = size[1]

print(f"Image is {x_max} by {y_max} pixels")

lis = []
x = 0
y = 0

while (x < x_max):
    while (y < y_max):
        lis.append([x, y, im.getpixel((x,y))])
        y += 1

    x += 1
    y = 0

os.remove('results.csv')
file = open('results.csv','w+')
file.write("x,y,r,g,b,rgbtotal\r\n")
result = []

pattern = re.compile(r"\D")

for each in lis:
    x = each[0]
    y = each[1]
    rgb = str(each[2]).split(",")

    r = pattern.sub('', rgb[0])
    g = pattern.sub('', rgb[1])
    b = pattern.sub('', rgb[2])

    result.append([x,y,r,g,b])

result = sorted(result)

for each in result:
    total = int(each[2]) + int(each[3]) + int(each[4])
    string = str(each[0]) + ',' + str(each[1]) + ',' + str(total) + '\n'

    file.write(writeme)

