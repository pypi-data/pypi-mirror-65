'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: setup.py
@time: 2019-09-06 10:31:15
@desc: 
'''
from setuptools import setup, find_packages

setup(
    name = 'pyjjzhktools',
    version = '1.5.4',
    keywords='jjzhk tools',
    description = 'a library',
    license = 'MIT License',
    url = 'https://gitlab.com/jjzhk-group/tools/pyjjzhktools',
    author = 'Jeff K Zhang',
    author_email = 'jeffcobile@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['PyYAML'],
)