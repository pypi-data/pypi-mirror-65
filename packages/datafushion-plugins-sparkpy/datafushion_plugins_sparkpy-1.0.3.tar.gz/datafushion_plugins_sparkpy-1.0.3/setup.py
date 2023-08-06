#  Copyright (c) XiaoLinpeng 2020.

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py    
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-09 07:06   肖林朋      1.0         打包分发
"""

from setuptools import setup, find_packages


filepath = 'README.md'

setup(
        name='datafushion_plugins_sparkpy',
        version='1.0.3',
        description="DataFushion的SparkPy算法插件",
        long_description=open(filepath, encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        license="XiaoLinpeng Licence",
        author="肖林朋",
        author_email="1553990434@qq.com",
        packages=find_packages(),
        include_package_data=True,
        zip_safe=True,
        platforms="any",
        install_requires=['datafushion-plugins-python'],
        data_files=[filepath],
        entry_points=
        {
            'console_scripts':
                [
                    '-v=datafushion_spark.version:version',
                ]
        },
)
