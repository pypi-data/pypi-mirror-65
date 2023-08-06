'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: dataset.py
@time: 2020-03-27 15:24:07
@desc: 
'''
import os
from jjzhk.config import ZKCFG
import tqdm
import cv2
import xml.etree.ElementTree as ET
import pycocotools.coco as coco
import zipfile
import numpy as np


class DataSetBase(object):
    def __init__(self, root,imageset, isSegmentation):
        self._root_path = root
        self._imageset = imageset
        self._img_list = []
        self._isSegmentation = isSegmentation
        self.__prepare__()

    def __len__(self):
        return len(self._img_list)

    def __getitem__(self, index):
        image = self.getImage(index)
        label = self.getLabel(index)
        if self._isSegmentation:
            mask = self.getMask(index)
            return image, label, mask

        return image, label

    def __prepare__(self):
        self.prepare()

    def __getItemInfo__(self, index):

        return self._img_list[index]

    def __getItemInfoByImageId__(self, imgid):
        pass

    def __getIndexByImageId__(self, imgid):
        index = 0
        for item in self._img_list:
            if item["img_id"] == imgid:
                return index

            index += 1

        return -1

    def prepare(self):
        pass

    def getImage(self, index):
        pass

    def getLabel(self, index):
        pass

    def getMask(self, index):
        pass


class VOCDataSet(DataSetBase):
    def __init__(self, config:ZKCFG, imageset, isSegmentation):
        root = os.path.join(config.BASE.DATA_ROOT, config.BASE.DATA_SUB_ROOT)
        self.dataConfig = config
        super(VOCDataSet, self).__init__(root=root, imageset=imageset, isSegmentation=isSegmentation)

    def prepare(self):
        prefix = "seg" if self._isSegmentation else "det"
        image_list_file = os.path.join(self._root_path, "MainSet", "%s_%s.txt" % (prefix, self._imageset))
        lines = [x.strip() for x in open(image_list_file, 'r').readlines()]

        bar = tqdm.tqdm(lines)
        for line in bar:
            bar.set_description("Processing %s" % self._imageset)
            l = self.__getItemInfoByImageId__(line)
            self._img_list.append(l)

    def getImage(self, index):
        fname = os.path.join(self._root_path, "JPEGImages", "%s.jpg" % self._img_list[index]["img_id"])
        self._img_list[index]["path"] = fname
        return cv2.imread(fname)

    def getLabel(self, index):
        return self._img_list[index]["boxes"]

    def getMask(self, index):
        info = self._img_list[index]
        file_index = info["img_id"]
        lbl_path = os.path.join(self._root_path, 'SegmentationDecode', file_index + '.png')
        label_mask = cv2.imread(lbl_path, cv2.IMREAD_GRAYSCALE)

        return label_mask

    '''
    {
        img_id : "***",
        width : "***",
        height : "***",
        boxes : [[classs_id, xmin, ymin, xmax, ymax],[classs_id, xmin, ymin, xmax, ymax]
        detail : [{"name":***,"pose":***, "truncated":***,"difficult":***,},{....},{....}]
        ...]
    }
    '''
    def __getItemInfoByImageId__(self, image_id):
        image_info = {}
        image_info["img_id"] = image_id
        labels = []
        detail = []
        anno_file = os.path.join(self._root_path, "Annotations", "%s.xml" % image_id)
        root = ET.parse(anno_file).getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        image_info["width"] = w
        image_info["height"] = h

        for obj in root.iter('object'):
            class_name = obj.find('name').text
            xmlbox = obj.find('bndbox')
            left   = int(xmlbox.find('xmin').text)
            right  = int(xmlbox.find('xmax').text)
            top    = int(xmlbox.find('ymin').text)
            bottom = int(xmlbox.find('ymax').text)
            class_id = self.dataConfig.classid(class_name)
            item = [class_id, left, top, right, bottom]
            labels.append(item)

            pose = obj.find("pose").text
            truncated = int(obj.find("truncated").text)
            difficult = int(obj.find("difficult").text)
            detail.append({"name": class_name, "pose":pose, "truncated" : truncated, "difficult" : difficult})

        image_info["boxes"] = labels
        image_info["detail"] = detail

        return image_info


class COCODataSet(DataSetBase):
    def __init__(self, config:ZKCFG, imageset, isSegmentation):
        self.dataConfig = config
        self.year = 2017
        super(COCODataSet, self).__init__(root=os.path.join(config.BASE.DATA_ROOT, config.BASE.DATA_SUB_ROOT), imageset=imageset, isSegmentation=isSegmentation)
        prefix = "%s%d" % (self._imageset, self.year)
        self.zip = zipfile.ZipFile(os.path.join(self._root_path, "%s.zip" % (prefix) ))

    def prepare(self):
        prefix = "%s%d" % (self._imageset, self.year)
        annFile = os.path.join(self._root_path, "annotations", "instances_%s.json" % prefix)
        print(annFile)
        self.coco = coco.COCO(annFile)
        class_ids = sorted(self.coco.getCatIds()) # all classes

        lines = []
        for id in class_ids:
            lines.extend(list(self.coco.getImgIds(catIds=[id])))
        # Remove duplicates
        lines = list(set(lines))

        bar = tqdm.tqdm(lines)
        for line in bar:
            bar.set_description("Processing %s" % self._imageset)
            l = self.__getItemInfoByImageId__(line)
            self._img_list.append(l)

    def getImage(self, index):
        info = self._img_list[index]
        img_info = self.coco.imgs[info["img_id"]]
        self._img_list[index]["path"] = ""
        prefix = "%s%d" % (self._imageset, self.year)
        r = self.zip.read('%s/%s' % (prefix, img_info['file_name']))
        arr = cv2.imdecode(np.frombuffer(r, np.uint8), 1)

        return arr

    def getLabel(self, index):
        return self._img_list[index]["boxes"]

    def getMask(self, index):
        info = self._img_list[index]
        img_id = info['img_id']
        height = info['height']
        width = info['width']
        annIds = self.coco.getAnnIds(imgIds=img_id, iscrowd=None)
        anns = self.coco.loadAnns(annIds)
        MASK = np.zeros((height, width), dtype=np.uint16)

        for i, ann in enumerate(anns):
            mask = self.coco.annToMask(ann)
            idxs = np.where(mask > 0)
            MASK[idxs] = ann['category_id']

        return MASK

    '''
    {
        img_id : "***",
        width : "***",
        height : "***",
        boxes : [[classs_id, xmin, ymin, xmax, ymax],[classs_id, xmin, ymin, xmax, ymax]
        ...]
    }
    '''
    def __getItemInfoByImageId__(self, image_id):
        image_info = self.coco.imgs[image_id]
        img_info_json = {}
        img_info_json["img_id"] = image_id
        img_info_json["width"] = image_info["width"]
        img_info_json["height"] = image_info["height"]
        class_coco = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                      55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
                      82, 84, 85, 86, 87, 88, 89, 90]
        annIds = self.coco.getAnnIds(imgIds=image_id, iscrowd=None)
        ann_info = self.coco.loadAnns(annIds)
        item = []
        for ann in ann_info:
            class_id = [class_coco.index(int(ann["category_id"]))]
            bbox = ann["bbox"]
            bbox[2] = bbox[0] + bbox[2]
            bbox[3] = bbox[1] + bbox[3]
            item.append(class_id + bbox + [1 if ann['iscrowd'] == 1 else 0])
        img_info_json["boxes"] = item
        img_info_json["anno"] = ann_info
        return img_info_json


class TestImageDataSet(DataSetBase):
    def __init__(self, cfg:ZKCFG, isSegmentation=False):
        self.cfg = cfg
        super(TestImageDataSet, self).__init__(root=cfg.BASE.TEST_DATA_ROOT, imageset='test', isSegmentation=isSegmentation)

    def prepare(self):
        image_list_file = os.path.join(self._root_path, "info.txt")
        lines = [x.strip() for x in open(image_list_file, 'r').readlines()]

        bar = tqdm.tqdm(lines)
        for line in bar:
            bar.set_description("Processing %s" % self._imageset)
            self._img_list.append({"img_id" : line})

    def getImage(self, index):
        fname = os.path.join(self._root_path, "Images", "%s.jpg" % self._img_list[index]["img_id"])
        image = cv2.imread(fname)
        self._img_list[index]["path"] = fname
        self._img_list[index]["height"] = image.shape[0]
        self._img_list[index]["width"] = image.shape[1]
        return image

    def getLabel(self, index):
        return None

    def getMask(self, index):
        return None