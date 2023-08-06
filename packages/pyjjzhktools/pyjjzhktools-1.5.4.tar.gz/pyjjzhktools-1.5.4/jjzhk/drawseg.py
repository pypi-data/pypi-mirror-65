'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: drawseg.py
@time: 2020-03-27 13:42:54
@desc: 
'''
import numpy as np
import PIL.ImageDraw as pil_imagedraw
import PIL.ImageFont as pil_imagefont
import PIL.Image as Image
import jjzhk.imageutils as eui
from jjzhk.config import ZKCFG
import cv2
import os


class BaseDrawSeg:
    def __init__(self,cfg:ZKCFG, output=str):
        '''
        :param classinfo:
        {
            "classlabel" : "color" # the first node should be background
        }
        :param output: path which images to save
        '''
        self.cfg = cfg
        self.output = output
        if not os.path.exists(self.output):
            os.mkdir(self.output)

    def drawByImage(self, image, boxes, mask, imagename):
        image_type = type(image)
        if image_type == np.ndarray:
            img = Image.fromarray(np.uint8(image * 255))
        elif image_type == str:
            image = cv2.imread(image)
            cv2topil = eui.CV2ToPIL()
            img = cv2topil(image)
        elif image_type == Image.Image:
            img = image
        else:
            raise ValueError("drawByImage just support str,ndarray and PIL.Image types")

        return self._draw_(img, boxes, mask, imagename)

    def _draw_(self, image, boxes, mask, imagename):
        img, mask = self._draw_box_(image, boxes, mask)

        img.save(os.path.join(self.output, "%s.jpg" % imagename))
        if mask is not None:
            mask.save(os.path.join(self.output, "%s_mask.jpg" % imagename))

    def _draw_box_(self, image, boxes, mask):
        font = pil_imagefont.truetype(font='Courier.dfont',
                                      size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 300
        if boxes is not None:
            for (x1, y1), (x2, y2), class_name, _, prob in boxes:
                draw = pil_imagedraw.Draw(image)
                left = int(x1)
                top = int(y1)
                right = int(x2)
                bottom = int(y2)
                color = tuple(self.cfg.color(class_name))

                label = '{} {:.2f}'.format(class_name, prob)
                label_size = draw.textsize(label, font)

                for i in range(thickness):
                    draw.rectangle(
                        [left + i, top + i, right - i, bottom - i], outline=color)

                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - label_size[1]])
                else:
                    text_origin = np.array([left, top + 1])

                draw.rectangle(
                    [tuple(text_origin), tuple(text_origin + label_size)],
                    fill=color)
                draw.text(text_origin, label, fill=(255, 255, 255), font=font)
                del draw

        if mask is not None:
            mask = cv2.cvtColor(self._maskToImg_(mask), cv2.COLOR_RGB2BGR)
            piltocv2 = eui.PILToCV2()
            image = piltocv2(image)
            image = cv2.addWeighted(image, 0.6, mask, 0.4, 0)
            cv2topil = eui.CV2ToPIL()
            image = cv2topil(image)
            mask = cv2topil(mask)
        return image, mask

    def _maskToImg_(self, mask):
        r = mask.copy()
        g = mask.copy()
        b = mask.copy()
        CLASS = self.cfg.BASE.CLASSINFO.keys()
        for ll, classname in enumerate(CLASS):
            if ll == 0:
                continue
            r[mask == ll] = self.cfg.color(classname)[0]
            g[mask == ll] = self.cfg.color(classname)[1]
            b[mask == ll] = self.cfg.color(classname)[2]

        rgb = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
        rgb[:, :, 0] = r
        rgb[:, :, 1] = g
        rgb[:, :, 2] = b

        return rgb