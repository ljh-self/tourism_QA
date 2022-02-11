import csv
import os
from elasticsearch import Elasticsearch, helpers

fileheader = ['question','answer']
contents = []
answer = '我也不知道呢'
index = 'qa'
document = 'qaexer01'

def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
def insert_csv_to_es(csvFile, index, doc_type):
    with open(csvFile, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(get_conn(), reader, index=index, doc_type=doc_type)
def save_contents(contents, writer):
    writer.writerow(contents)
def download(filename):
    global fileheader, contents
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        if not os.stat(filename).st_size > 0:
            csv_writer.writerow(fileheader)
        save_contents(contents, csv_writer)
def teach_to_robot(question, next_talk):
    global contents, answer
    contents = []
    if answer == '我也不知道呢':
        if '答案是' in next_talk:
            answer = next_talk.replace('答案是','')
            question = question
            contents.append(question)
            contents.append(answer)
            download('teach.csv')
            insert_csv_to_es('teach.csv', index, document)
def dsl_search_qa(value):
    dsl = {
        "query": {
            "match": {
                "question": value
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