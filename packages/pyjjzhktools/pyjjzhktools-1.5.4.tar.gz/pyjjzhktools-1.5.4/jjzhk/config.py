'''
@author: JJZHK
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: Config.py
@time: 2018/12/11 10:18
@desc: 
'''
import os
import yaml
import json


class YamlConfig(object):
    def __init__(self, config_dict:dict):
        for key, val in config_dict.items():
            if isinstance(val, dict):
                self.__setattr__(key, YamlConfig(val))
            elif isinstance(val, list):
                self.__setattr__(key, [])
                for obj in val:
                    if isinstance(obj, dict):
                        self[key].append(YamlConfig(obj))
                    else:
                        self[key].append(obj)
            else:
                self.__setattr__(key, val)

    def copy(self, new_config_dict={}):
        ret = YamlConfig(vars(self))
        for key, val in new_config_dict.items():
            ret.__setattr__(key, val)

        return ret

    def replace(self, new_config_dict):
        for key in new_config_dict.keys():
            val = new_config_dict[key]
            if isinstance(val, YamlConfig):
                if hasattr(self, key):
                    self[key].replace(val)
                else:
                    self.__setattr__(key, val)
            else:
                self.__setattr__(key, val)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def keys(self):
        return list(vars(self).keys())

    def values(self):
        return list(vars(self).values())

    def print(self):
        for k, v in vars(self).items():
            print(k, ' = ', v)


class ZKCFG:
    def __init__(self,basefile:str, cfgfile:str, rootpath='cfgs'):
        self._base_file_ = None
        self._cfg_file_ = None
        self.CFGData = None

        if basefile is not None:
            with open(os.path.join(rootpath, basefile), 'r') as file:
                data = yaml.load(file,Loader=yaml.FullLoader)
                self._base_file_ = YamlConfig(data)

        if cfgfile is not None:
            with open(os.path.join(rootpath, cfgfile), 'r') as file:
                data = yaml.load(file,Loader=yaml.FullLoader)
                self._cfg_file_ = YamlConfig(data)

        assert self._base_file_ is not None or self._cfg_file_ is not None

        if self._base_file_ is None:
            self.CFGData = self._cfg_file_
        elif self._cfg_file_ is None:
            self.CFGData = self._base_file_
        else:
            self._base_file_.replace(self._cfg_file_)
            self.CFGData = self._base_file_

    def __getattr__(self, name):
        return self.CFGData[name]

    def __getitem__(self, key):
        return self.CFGData[key]

    def color(self, classname:str):
        return self.CFGData.BASE.CLASSINFO[classname]

    def classname(self,idx:int):
        return self.CFGData.BASE.CLASSINFO.keys()[idx]

    def classid(self, classname:str):
        return self.CFGData.BASE.CLASSINFO.keys().index(classname)

    def print(self):
        self.CFGData.print()
# class Config:
#     def __init__(self, cfgfile, commonfile=None, cfgroot="cfgs/", loadtype='f'):
#         '''
#         :param commonfile: 公共部分的文件地址或字符串
#         :param cfgfile: 需要加载的yml文件名或字符串
#         :param cfgroot: yml目录地址
#         :param loadtype: 加载方式：f-yml文件加载，s-字符串加载
#         '''
#         self.commonfile = commonfile
#         self.loadtype = loadtype
#         self.cfgroot = cfgroot
#         self.CFGData = AttrDict({})
#         if self.loadtype == 'f':
#             with open(os.path.join(cfgroot, cfgfile), 'r') as file:
#                 data = yaml.load(file, Loader=yaml.FullLoader)
#         elif self.loadtype == 's':
#             with open(os.path.join(cfgfile), 'r') as file:
#                 data = yaml.load(file,Loader=yaml.FullLoader)
#         else:
#             raise Exception("Load type is error.")
#
#         data = json.loads(json.dumps(data))
#         self.CFGData = AttrDict(data)
#         if self.commonfile is not None:
#             self._initcfg_()
#
#         self._mergecfg_(self.CFGData, AttrDict(data))
#
#         self._updatecfg_()
#
#     def _initcfg_(self):
#         if self.loadtype == 'f':
#             with open(os.path.join(self.cfgroot, self.commonfile), 'r') as file:
#                 data = yaml.load(file, Loader=yaml.FullLoader)
#         elif self.loadtype == 's':
#             data = yaml.load(self.commonfile, Loader=yaml.FullLoader)
#         else:
#             raise Exception("Load type is error.")
#
#         data = json.loads(json.dumps(data))
#         self.CFGData = AttrDict(data)
#         self._initspecial_()
#
#     def _mergecfg_(self,target, data):
#         target.merge(data)
#
#     def _updatecfg_(self):
#         pass
#
#     def _initspecial_(self):
#         pass


# class DataConfig:
#     def __init__(self, cfg=Config):
#         self.cfg = cfg
#         self.classinfo = self.cfg.BASE.CLASSINFO
#
#         self.colors = list(self.classinfo.todict().values())
#         self.classes = list(self.classinfo.todict().keys())
#         if self.classes[0] == 'background':
#             self.classes.remove('background')
#
#         self.classes_num = len(self.classes)
#         self.dataset = None
#         self.name = self.cfg.BASE.DATA_TYPE
#
#     def getClasses(self):
#
#         return self.classes
#
#     def getColors(self):
#         return self.colors
#
#     def getNumByClass(self, cls):
#         classes = self.getClasses()
#         return classes.index(cls)
#
#     def getClassByNum(self, num):
#         classes = self.getClasses()
#         return classes[num]


# if __name__ == '__main__':
#     cfg = ZKCFG(basefile='basic_config_voc.yml', cfgfile="vgg16.yml", rootpath='')
#     # cfg.T = "CC"
#     # print(cfg.T)
