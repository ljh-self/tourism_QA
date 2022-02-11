import csv

import pyhanlp
from elasticsearch import helpers, Elasticsearch

from question_classfication.data_process_exer01 import Question
from question_classfication.question_template import QuestionTemplate
spot = ''
# csvFile = r"C:\Users\dell\Desktop\mytest.csv"
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
def insert_csv_to_es(csvFile, index, doc_type):
    with open(csvFile, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(get_conn(), reader, index=index, doc_type=doc_type)

def multiple_rounds(new_question):
    global spot
    flag = True
    new_list = pyhanlp.HanLP.segment(new_question)
    for item in new_list:
        if str(item).endswith('/ns'):
            spot = str(item).split('/')[0]
            answer = Question().question_process(new_question)
            print(answer)
            flag = False
            break
    if flag:
        new_question = str(spot) + new_question
        answer = Question().question_process(new_question)
        print(answer)

if __name__ == '__main__':
    question = "灵隐寺的开放时间是什么"
    multiple_rounds(question)
    question = "票价是多少"
    multiple_rounds(question)
    question = "西湖的地址是哪里"
    multiple_rounds(question)