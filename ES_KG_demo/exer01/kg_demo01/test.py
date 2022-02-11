#-*- coding: UTF-8 -*-
# @Time    : 2019/4/13 20:49
# @Author  : xiongzongyang
# @Site    : 
# @File    : mytest.py
# @Software: PyCharm
#
# def hello():
#     print("hello")
#
# def bye():
#     print("bye")
# b={0:hello,1:bye}
#
# b[0]()
#
# exit()

import sys
import pandas as pd
from pandas import Series, DataFrame
from ES_KG_demo.exer01.kg_demo01.preprocess_data import Question
# 创建问题处理对象，这样模型就可以常驻内存
que=Question()
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
enablePrint()
result=que.question_process("章子怡演过多少部电影")
print(result)