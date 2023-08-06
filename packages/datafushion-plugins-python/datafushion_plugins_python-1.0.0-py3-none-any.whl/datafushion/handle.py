#  Copyright (c) XiaoLinpeng 2020.

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   handle.py    
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-09 19:12   肖林朋      1.0         数据处理封装闭包管理器
"""
from datafushion.args import ArgStruct
from datafushion.parse_utils import parse_file_2_map_list

from contextlib import contextmanager
import json
import sys


@contextmanager
def operation():
    """
    数据处理封装
    :return:
    """


    def destruction():
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
            file_input_mapping = input_struct.mapping2Json()
            data_list = parse_file_2_map_list(file_path, file_type)
            input_data_struct_list.append({
                "file_type":          file_type,
                "file_path":          file_path,
                "file_input_mapping": file_input_mapping,
                "data_list":          data_list
            })

        return {
            "input_data_struct_list": input_data_struct_list,
            "output_path":            output_path,
            "param_map":              param_map,
            "data_result":            None
        }


    def save_data(data_result, output_path):
        """
        存储数据
        :param data_result: 已处理好的数据
        :param output_path:  输出路径
        :return:
        """
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(data_result, f)


    destruction = destruction()
    yield destruction

    save_data(destruction['data_result'], destruction['output_path'])
