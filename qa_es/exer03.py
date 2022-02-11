import csv
import os

import docx
from elasticsearch import Elasticsearch, helpers

fileheader = ['name', 'content']
def get_docx_content(filePath):
    boldtext = []
    contenttext = []
    doc = docx.Document(filePath)
    for p in doc.paragraphs:
        for r in p.runs:
            if r.bold:
                boldtext.append(r.text)
            else:
                contenttext.append(r.text)
    return boldtext, contenttext
def save_contents(contents, writer):
    writer.writerow(contents)

def download(filename):
    global fileheader

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        if not os.stat(filename).st_size > 0:
            csv_writer.writerow(fileheader)
        bold, content = get_docx_content('1.docx')
        for i in range(len(bold)):
            contents = []
            contents.append(bold[i])
            contents.append(content[i])
            save_contents(contents, csv_writer)
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
def insert_csv_to_es(csvFile, index, doc_type):
    with open(csvFile, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(get_conn(), reader, index=index, doc_type=doc_type)
if __name__ == '__main__':
    download('1.csv')
    insert_csv_to_es('1.csv', 'exer03', 'myexer03')