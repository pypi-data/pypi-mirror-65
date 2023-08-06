#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import setuptools

# the name PyFace is used
# use PyFaceDet instead :P
setuptools.setup(
    name='easyface',
    version='0.1.0',
    author='zhuzhuangtian',
    author_email='576583342@qq.com',
    url='https://github.com/zjuxumang/PyFace',
    description='fork自zxxml的PyFace项目，增加了对python版本的检查，避免了windows系统下使用32-bit python报错的问题。底层使用了yushiqi开源的libfacedetection。具体使用方法见github',
    packages=setuptools.find_packages(),
    package_data={'': ['*.dll', '*.so']},
    install_requires=['numpy', 'Pillow']
)
