'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: device.py
@time: 2020-03-31 18:21:21
@desc: 
'''
import torch

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')