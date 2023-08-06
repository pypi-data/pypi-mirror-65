'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: imageutils.py
@time: 2019-09-06 10:33:48
@desc: 
'''
import PIL.Image as Image
import cv2
import numpy as np
import os
import imageio


class CV2ToPIL:
    def __init__(self):
        pass

    def __call__(self, image):
        image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        return image


class PILToCV2:
    def __init__(self):
        pass

    def __call__(self, image):
        image = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
        return image


class ImageToGif:
    def __init__(self):
        pass

    def __call__(self, imagefolder, duration=0.1, **kwargs):
        filenames = sorted(
            (os.path.join(imagefolder, fn) for fn in os.listdir(imagefolder) if fn.endswith('.png') or fn.endswith('.jpg')))
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('{}.gif'.format(filename[:filename.rfind('.')]), images, duration=duration)