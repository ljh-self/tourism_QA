import xlrd

import jpype
import pyhanlp
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import jieba
from hanlp import hanlp_exer01
from es_demo import es_exer03

from mytest.test01.preprocess_data import Question
from mytest.test01.question_classification import Question_classify


def getInfo_excel(filePath):
    global rightCnt
    rightCnt = 0
    data = xlrd.open_workbook(filePath)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    qc = Question_classify()
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue

        test_sentence = table.row_values(i)[0]
        id = str(table.row_values(i)[1])[0]
        # print(id)
        ans = str(qc.predict(test_sentence) - 10)
        # print(ans)
        if ans == id:
            rightCnt = rightCnt + 1
    return  rightCnt * 100 / (nrows - 1)

def getAnswer_excel(filePath):
    data = xlrd.open_workbook(filePath)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    # qc = Question_classify()
    for i in range(nrows - 195):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        test_sentence = table.row_values(i)[0]
        answer = Question().question_process(test_sentence)
        print(answer)

if __name__ == '__main__':
    # print(getInfo_excel('C:\\Users\\dell\\Desktop\\mytest.xls'))
    getAnswer_excel('C:\\Users\\dell\\Desktop\\test.xls')