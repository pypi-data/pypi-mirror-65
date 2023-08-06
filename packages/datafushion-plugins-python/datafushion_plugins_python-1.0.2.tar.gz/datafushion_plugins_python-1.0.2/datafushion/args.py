#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   args.py
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-08 21:26   肖林朋      1.0         参数相关实体类
"""

import json
from enum import Enum


#  Copyright (c) XiaoLinpeng 2020.

class ArgStruct(object):
    """
    总参数结构体
    """


    def __init__(self):
        self.param = None
        self.output = None
        self.input = None


    @staticmethod
    def parse(arg):
        """
        解析参数
        :param arg: 参数数组
        :return: 参数结构体对象
        """
        length = len(arg)
        struct = ArgStruct()
        if length == 1:
            struct.input = arg[0]
        elif length == 2:
            struct.input = arg[0]
            struct.output = arg[1]
        elif length == 3:
            struct.input = arg[0]
            struct.output = arg[1]
            struct.param = arg[2]
        return struct


    def get_input(self):
        """
        获取可用的输入,由于Linux环境可能对引号敏感
        :return: 规范化输入
        """
        new_input = self.input.replace("**", "\"")
        if "}}]" not in new_input:
            new_input = new_input.replace("]", "}}]")
        return new_input


    def get_output(self):
        """
        获取可用的输出,由于Linux环境可能对引号敏感
        :return: 规范化输出
        """
        return self.output.replace("**", "\"")


    def get_param(self):
        """
        获取可用的参数,由于Linux环境可能对引号敏感
        :return: 规范化参数
        """
        return self.param.replace("**", "\"")


    def fetch_input_structs(self):
        """
        获取输入结构体
        :return:
        """
        res = []
        if self.input is not None:
            for item in json.loads(self.get_input()):
                input_struct = InputStruct()
                input_struct.file_path = item['filePath']
                input_struct.file_format = item['fileFormat']
                input_struct.mapping = item['mapping']
                res.append(input_struct)
        return res


    def fetch_param_map(self):
        """
        获取参数Map
        :return:
        """
        res = {}
        if self.param is not None:
            res = ParamParse.parse_params(self.param)
        return res


    def fetch_output_path(self):
        """
        获取输出路径
        :return: 输出路径
        """
        return self.output


class InputStruct(object):
    """
    输入结构体
    """


    def __init__(self):
        self.file_path = None
        self.file_format = None
        self.mapping = None


    def mapping_2_json(self):
        """
        mapping的字符串转换为Json对象
        :return: json对象
        """
        return self.mapping


class ParamEnum(Enum):
    """
    参数枚举
    """
    STRING = 'String'
    INT = 'Int'
    DOUBLE = 'Double'


class FileExtractFormatEnum(Enum):
    """
    文件提取格式枚举
    """
    JSON = "json"
    CSV = "csv"
    GENERAL = "general"
    PARQUET = "parquet"


class ParamParse(object):
    """
    参数结构体
    """


    @staticmethod
    def parse_params(params):
        """
        解析参数
        :param params: 参数字符串
        :return: 参数Map
        """
        param_map = {}
        param_splits = params.split(',')
        for param_body in param_splits:
            key_value_splits = param_body.split("->")
            key = key_value_splits[0]
            value_body = key_value_splits[1]

            value_type_splits = value_body.split(":")
            param_type = value_type_splits[1]

            if ParamEnum.STRING.value == param_type:
                param_map[key] = value_type_splits[0]
            elif ParamEnum.INT.value == param_type:
                param_map[key] = int(value_type_splits[0])
            elif ParamEnum.DOUBLE.value == param_type:
                param_map[key] = float(value_type_splits[0])

        return param_map
