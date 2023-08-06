#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   handle.py    
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-10 18:57   肖林朋      1.0         功能描述
"""

#  Copyright (c) XiaoLinpeng 2020.

# !/usr/bin/env python
# -*- encoding: utf-8 -*-

from datafushion.args import ArgStruct
from datafushion.handle import HandleDataSet, HandleInputDataStruct

from contextlib import contextmanager
import sys
from pyspark.sql import SparkSession, DataFrame


class HandleDataFrameSet(HandleDataSet):
    def __init__(self, input_data_struct_list, output_path, param_map, data_result, output_type, spark):
        super().__init__(input_data_struct_list, output_path, param_map, data_result)
        self.output_type = output_type
        self.spark = spark


@contextmanager
def operation(app_name, master="yarn-cluster"):
    """
    数据处理封装
    :return:
    """
    spark = SparkSession.builder \
        .appName("Python Spark SQL basic example") \
        .master(master) \
        .appName(app_name) \
        .getOrCreate()

    # 文件抽取方法
    file_extract_dict = dict(
            json=lambda file_path, data_columns: spark.read.json(path=file_path, multiLine=True).select(data_columns),
            csv=lambda file_path, data_columns: spark.read.csv(path=file_path, multiLine=True, header=True).select(
                    data_columns),
            parquet=lambda file_path, data_columns: spark.read.parquet(file_path).select(data_columns),
            general=lambda file_path, data_columns: spark.read.text(paths=file_path, wholetext=True).withColumnRenamed(
                    "value", data_columns[0]))

    # 文件保存方法
    file_save_dict = dict(
            json=lambda data_result, output_path: data_result.write.json(path=output_path, mode="overwrite",
                                                                         multiLine=True),
            csv=lambda data_result, output_path: data_result.write.csv(path=output_path, mode="overwrite",
                                                                       header=True, multiLine=True),
            parquet=lambda data_result, output_path: data_result.write.parquet(path=output_path, mode="overwrite"),
            general=lambda data_result, output_path: data_result.select("value").write.mode('overwrite').text(
                    output_path))


    def destruction() -> HandleDataFrameSet:

        """
        处理输入,输入可以有多个数据集
        :return: 输出处理结构体,输入数据集合,输出路径,参数Map
        """
        args = None
        if len(sys.argv) == 3:
            args = [sys.argv[1], sys.argv[2], None]
        elif len(sys.argv) == 4:
            args = [sys.argv[1], sys.argv[2], sys.argv[3]]

        arg_struct = ArgStruct.parse(args)
        input_structs = arg_struct.fetch_input_structs()
        output_path = arg_struct.fetch_output_path()
        param_map = arg_struct.fetch_param_map()

        input_data_struct_list = []
        for input_struct in input_structs:
            file_type = input_struct.file_format
            file_path = input_struct.file_path
            file_input_mapping = input_struct.mapping_2_json()  # type: dict
            del file_input_mapping['connectId']

            data_columns = list(file_input_mapping.values())
            mapping_columns = list(file_input_mapping.keys())

            data_frame = file_extract_dict[file_type](file_path, data_columns)

            data_list = data_frame.toDF(*mapping_columns)
            input_data_struct_list.append(HandleInputDataStruct(file_type=file_type, file_path=file_path,
                                                                file_input_mapping=file_input_mapping,
                                                                data_list=data_list))

        return HandleDataFrameSet(input_data_struct_list=input_data_struct_list, output_path=output_path,
                                  param_map=param_map, data_result=None, output_type=None, spark=spark)


    def save_data(data_result: DataFrame, output_path, output_type):
        """
        存储数据
        :param data_result: 已处理好的数据
        :param output_path:  输出路径
        :param output_type: 输出类型
        :return:
        """
        data_result.show()
        file_save_dict[output_type](data_result, output_path)


    destruction = destruction()
    yield destruction

    save_data(destruction.data_result, destruction.output_path, destruction.output_type)
