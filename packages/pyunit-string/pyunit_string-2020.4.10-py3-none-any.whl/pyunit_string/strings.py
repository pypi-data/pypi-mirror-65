#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/3/30 9:52
# @Author: Jtyoui@qq.com
# @site: 对字符串模块进行加强封装
import numbers
import json
import re


class Strings:

    def __init__(self, value: str = '', **kwargs):
        """
        kwargs 参数包括：
            - json_ :将字符串类型转为json格式
            - file  : 文件路径
        """
        self._kwargs = kwargs
        self.value = value

    @staticmethod
    def _change_str(other):
        if isinstance(other, numbers.Real):
            other = str(other)
        elif isinstance(other, numbers.Complex):
            other = str(other)
            if '(' in other:
                other = other[1:-1]
        return other

    def __add__(self, other):
        """加强两个属性，一个是可以加数字类型。另一个是可以加列表和元组。

        当字符串加列表或者元组是：

        >>> '#'+[1,2,3] #返回 1#2#3，类似于join
        """
        if isinstance(other, (list, tuple)):
            return self.join(other)
        else:
            other = self._change_str(other)
            obj = self.value + other
        return Strings(obj)

    def __iadd__(self, other):
        """加强+=模式，增加数字类型"""
        if isinstance(other, (list, tuple)):
            self.value = self.value.join(map(self._change_str, other))
        else:
            other = self._change_str(other)
            self.value += other
        return self

    def join(self, iterable):
        """增加数字类型"""
        iterable = map(self._change_str, iterable)
        obj = self.value.join(iterable)
        return Strings(obj)

    def json_dump(self, json_=None, file=None, **kwargs):
        """获取json格式

        :param json_: 需要转为json格式的数据
        :param file: 需要保存json数据的文件路径
        :param kwargs: 其余参数
        :return: json格式
        """
        json_ = json_ or self._kwargs.get('json_', {})
        file = file or self._kwargs.get('file')
        if file is not None:
            with open(file, mode='w', encoding='utf-8') as fp:
                obj = json.dump(json_, fp, **kwargs)
        else:
            obj = json.dumps(json_, **kwargs)
        return obj

    def json_load(self, json_=None, file=None, **kwargs):
        """加载json格式

        :param json_: 加载json格式的数据
        :param file: 需要加载json数据的文件路径
        :param kwargs: 其余参数
        :return: json格式
        """
        json_ = json_ or self._kwargs.get('json_', {})
        file = file or self._kwargs.get('file')
        if file is not None:
            with open(file, mode='r', encoding='utf-8') as fp:
                obj = json.load(fp, **kwargs)
        else:
            obj = json.loads(json_, **kwargs)
        return obj

    def __str__(self):
        return self.value

    def replace(self, old: str, new: str, count: int = 0, **kwargs):
        """正则替换"""
        obj = re.sub(old, new, self.value, count=count, **kwargs)
        return Strings(obj)

    def length(self):
        return len(self.value)

    def find(self, sub, start=0, end=None) -> list:
        """找到sub所有的索引，返回是所有索引的集合"""
        end = end or self.length()
        ls = []
        while start <= end:
            index = self.value.find(sub, start, end)
            if index > -1:
                ls.append(index)
                start = index + 1
            else:
                break
        return ls

    def __mul__(self, other):
        """加强相乘的功能

        如果other是列表：那么按到列表的索引对应的字符相乘

        >>> 'abc' * [1,2,3] #返回 abbccc


        如果other是字典，那么按到key的字符串进行相乘

        >>> 'abc' * {'a':1,'b':2,'c':3} #返回 abbccc

        """
        value = self.value
        if isinstance(other, int):
            value = value * other
        elif isinstance(other, (list, tuple)):
            if len(other) == self.length():
                ls = map(lambda x: value[x[0]] * x[1], enumerate(other))
                value = ''.join(ls)
            else:
                raise IndexError('列表的长度不等于字符串的长度，无法进行按索引相乘')
        elif isinstance(other, dict):
            for key, index in other.items():
                if key in value:
                    value = re.sub(key, key * index, value)
        return Strings(value)

    def distance(self, char1, char2) -> list:
        """计算两个字符间的距离

        比如：abc
        计算a和b之间的距离，返回是：[1]
        """
        char1_ls = self.find(char1)
        if char1_ls:
            char2_ls = self.find(char2)
            return [abs(x - y) - 1 for x in char1_ls for y in char2_ls]
        return []

    def list_subset_in_string(self, ls, force=False) -> bool:
        """列表中的子集在字符串中
        例如：list [a,b,c,d]，字符串：vid
        d in vid 中返回true

        :param ls: 列表
        :param force: 是否全部满足
        :return: 返回布尔值
        """
        forces = all if force else any
        value = map(lambda x: x in self.value, ls)
        return forces(value)

    def string_in_list_subset(self, ls, force=False) -> bool:
        """列表中的子集在字符串中
        例如：list [abc,bbc,bc,dbc]，字符串：bc
        bc in abc 中返回true

        :param ls: 列表
        :param force: 是否全部满足
        :return: 返回布尔值
        """
        forces = all if force else any
        value = map(lambda x: self.value in x, ls)
        return forces(value)
