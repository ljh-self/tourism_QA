import pyhanlp
from elasticsearch import Elasticsearch
index3 = 'myexer03'
document3 = 'exer03'
adult_list = ['成年人', '大人', '成年']
child_list = ['儿童', '孩子', '小孩']
elder_list = ['老人', '老年人']

def get_person_num(list, i):
    num = 0
    min_dis = 5
    for j in range(len(list)):
        if str(list[j]).endswith('/m'):
            if abs(j - i) < min_dis:
                min_dis = abs(j - i)
                num = str(list[j]).replace('/m', '')
    return int(num)
def get_cost(sentence):
    list = pyhanlp.HanLP.segment(sentence)
    adult = []
    child = []
    elder = []
    # sale = []
    adult_cost = 0
    child_cost = 0
    elder_cost = 0
    adult_ticket, child_ticket, elder_ticket, sale_ticket = search_scense_ticket_by_name(sentence)
    for i in range(len(list)):
        if str(list[i]).endswith('/n'):
            name = str(list[i]).replace('/n', '')
            if name in adult_list:
                adult.append(name)
                num = get_person_num(list, i)
                adult.append(num)
                adult_cost = num * float(adult_ticket)
            if name in child_list:
                child.append(name)
                num = get_person_num(list, i)
                child.append(num)
                child_cost = num * float(child_ticket)
            if name in elder_list:
                elder.append(name)
                num = get_person_num(list, i)
                elder.append(num)
                elder_cost = num * float(elder_ticket)
    cost = adult_cost + child_cost + elder_cost - float(sale_ticket)
    return cost
def get_scense_name(sentence):
    list = pyhanlp.HanLP.segment(sentence)
    for i in range(len(list)):
        if str(list[i]).endswith('/ns'):
            name = str(list[i]).replace('/ns', '')
            return name
def dsl_search_name(value):
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    return dsl
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
def search_scense_ticket_by_name(sentence):
    name = get_scense_name(sentence)
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index3, doc_type=document3)
    ticket = dict(result['hits']['hits'][0]['_source']['ticket'])
    # print(name + '景区成人票价为' + ticket.get('adult') + '每人，' + '儿童票价为' + ticket.get('child') + '每人。')
    return ticket.get('adult'), ticket.get('child'), ticket.get('elder'), ticket.get('sale')

if __name__ == '__main__':
    test_sentence = "去西湖游玩，我们大人5个孩子2个需要多少钱"
    print(get_cost(test_sentence))