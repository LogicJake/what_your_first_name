# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2018-11-27 14:51:40
# @Last Modified time: 2018-11-28 17:20:27
import random
from math import sqrt
import os
import shutil
import sys
from PIL import Image, ImageDraw, ImageFont


num_a = 25
num_b = int(sqrt(num_a))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def prepare_data():
    names = []

    with open(resource_path(os.path.join('resources', 'name.txt')), 'r') as f:

        lines = f.readlines()

        for single in lines:
            single = single.strip()
            name = single.split(" ")
            name = [n.ljust(3, ' ') for n in name]
            names.extend(name)

    random.shuffle(names)

    combinations = [names[i:i + num_a] for i in range(0, len(names), num_a)]

    cs = []
    for c in combinations:
        cs.append([c[i:i + num_b]
                   for i in range(0, len(c), num_b)])

    c_2 = []
    for i in range(num_a):
        row = i // num_b
        column = i % num_b
        temp = []
        for c in cs:
            # print(row, column, len(c), len(c[row]), c)
            if row < len(c) and column < len(c[row]):
                temp.append(c[row][column])
        random.shuffle(temp)
        c_2.append(temp)

    num_c = int(sqrt(len(c_2[0])))
    # print(c_2)
    c_2_s = []
    for c in c_2:
        c_2_s.append([c[i:i + num_c]
                      for i in range(0, len(c), num_c)])
    return cs, c_2_s


def save_fig(data1, data2):
    if os.path.exists(resource_path('fig')):
        shutil.rmtree(resource_path('fig'))

    os.makedirs(resource_path('fig'), exist_ok=True)

    image_width = 280
    image_height = 160

    images = []
    for index, data in enumerate(data1):
        text = str(index) + '\n'

        for line in data:
            text += ''.join(line)
            text += '\n'
        text += '\n'
        im = Image.new("RGB", (image_width, image_height), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(resource_path(
            os.path.join('resources', 'simsun.ttf')), 20)
        dr.text((0, 0), text, font=font, fill="#000000")
        images.append(im)

    num = int(sqrt(len(data1)))
    line = []
    for i in range(0, len(images), num):
        images_c = images[i: i + num]
        target = Image.new('RGB', (image_width * num, image_height), 'white')
        left = 0
        right = image_width
        for image in images_c:
            target.paste(image, (left, 0, right, image_height))
            left += image_width
            right += image_width
            quality_value = 100
        line.append(target)

    target = Image.new(
        'RGB', (image_width * num, image_height * len(line)), 'white')
    left = 0
    right = image_height
    for image in line:
        target.paste(image, (0, left, image_width * num, right))
        left += image_height
        right += image_height
        quality_value = 100
        target.save(resource_path(os.path.join(
            'fig', 'names.jpg')), quality=quality_value)

    for index, data in enumerate(data2):
        text = ''

        for line in data:
            text += ''.join(line)
            text += '\n'
        text += '\n'

        im = Image.new("RGB", (image_width, image_height), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(resource_path(
            os.path.join('resources', 'simsun.ttf')), 25)
        dr.text((0, 0), text, font=font, fill="#000000")
        im.save(resource_path(os.path.join('fig', 'card_{}.jpg'.format(index))),
                quality=quality_value)


def prepare():
    data1, data2 = prepare_data()
    save_fig(data1, data2)
    return data1

if __name__ == '__main__':
    prepare()
