import pyhanlp
from elasticsearch import Elasticsearch
from pinyin import get
from question_classfication.classfication_exer01 import Question_classify
from question_classfication.data_process_exer01 import Question
from question_classfication.insert_to_es import insert_csv_to_es
from spider_csv import spider_hzscense_exer02, spider_hzdetails_exer03
from talker_robot.exer04.teach04 import search_qa_answer, teach_to_robot
from talker_robot.exer04.mytalker04 import switch_func, update_online

index = 'KGindex'
document = 'KGdocument'
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
def dsl_search_qa(value):
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    return dsl

def search_qa_answer(question):
    dsl = dsl_search_qa(question)
    result = get_conn().search(dsl, index, doc_type=document)
    try:
        answer = result['hits']['hits'][0]['_source']['answer']
    except:
        answer = '我还不清楚'
    return str(answer)

def getinfo_online(question):
    global i
    name = ''
    url = 'https://hangzhou.cncn.com/jingdian/'
    list = pyhanlp.HanLP.segment(question)
    for item in list:
        if str(item).endswith('/ns'):
            name = str(item).replace('/ns', '')
            break
    # answer = Question().question_process(question)
    pyname = get(name, format='strip')
    i = Question_classify().predict(question)
    result = switch_func(i, url, pyname)
    update_online(question)
    return result
def search_es_kg(question):
    global value
    list = pyhanlp.HanLP.segment(question)
    for item in list:
        if str(item).endswith('/ns'):
            value = str(item).replace('/ns', '')
            break
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    result = get_conn().search(dsl, index, doc_type=document)
    try:
        answer = result['hits']['hits'][0]['_source']['answer']
    except:
        answer = '我还不清楚'
    return str(answer)



def search_kg_or_qa(question):
    if search_qa_answer(question) != '我还不清楚':
        return search_qa_answer(question)
    elif search_es_kg(question) != '我还不清楚':
        que = Question()
        result = que.question_process(question)
        return result
    else:
        return getinfo_online(question)
if __name__ == '__main__':
    question = "杭州西湖在哪里"

