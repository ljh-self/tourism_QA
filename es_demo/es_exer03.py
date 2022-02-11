from elasticsearch import Elasticsearch
# es中的索引名称
index1 = 'hzscense'
index2 = 'hzhistory'
# es中的文档名称
document1 = 'scense'
document2 = 'history'
# 获取es连接
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es

def dsl_search_name(value):
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    return dsl
def search_scense_address_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    address = result['hits']['hits'][0]['_source']['address']
    return name + '景区的地址为' + address
def search_scense_level_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    level = result['hits']['hits'][0]['_source']['level']
    return name + '景区的级别为' + level + '级'
def search_scense_type_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    type = result['hits']['hits'][0]['_source']['type']
    return name + '景区的类型为' + type
def search_scense_spot_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    spot = result['hits']['hits'][0]['_source']['spot']
    return name + '景区中有' + spot
def search_scense_opentime_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    opentime = dict(result['hits']['hits'][0]['_source']['opentime'])
    opent = opentime.get('opent')
    closet = opentime.get('closet')
    # start_time = result['hits']['hits'][0]['_source']['opentime'][0]
    # end_time = result['hits']['hits'][0]['_source']['opentime'][1]
    # return name + '景区开放时间为' + start_time + '到' + end_time
    return name + '景区开放时间为' + opent + '到' + closet
def search_scense_saletime_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    saletime = dict(result['hits']['hits'][0]['_source']['saletime'])
    startt = saletime.get('startt')
    endt = saletime.get('endt')
    return name + '景区售票时间为' + startt + '到' + endt
def search_scense_ticket_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    ticket = dict(result['hits']['hits'][0]['_source']['ticket'])
    return name + '景区成人票价为' + ticket.get('adult') + '每人，' + '学生票价为' + ticket.get('student') + '每人。'
def search_scense_description_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    description = dict(result['hits']['hits'][0]['_source']['description'])
    return description
def dsl_search_level(value):
    dsl = {
        "query": {
            "match": {
                "level": value
            }
        }
    }
    return dsl
def search_scense_name_by_level(level):
    dsl = dsl_search_level(level)
    result = get_conn().search(dsl, index1, doc_type=document1)
    hits = result['hits']['hits']
    name_list = ''
    for hit in hits:
        name_list = hit['_source']['name'] + '，' + name_list
    return '级别为' + level + '级的景区有' + name_list
def dsl_search_opentime(value1, value2):
    dsl = {
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "opentime": {
                            "gte": value1,
                            "lte": value2
                        }
                    }
                }
            }
        }
    }
    return dsl
def search_scense_name_by_opentime(open_time, close_time):
    dsl = dsl_search_opentime(open_time, close_time)
    result = get_conn().search(dsl, index1, doc_type=document1)
    hits = result['hits']['hits']
    name_list = ''
    for hit in hits:
        name_list = hit['_source']['name'] + '，' + name_list
    return '开放时间在' + open_time + '到' + close_time + '之间的景区有' + name_list
def dsl_search_saletime(value1, value2):
    dsl = {
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "saletime": {
                            "gte": value1,
                            "lte": value2
                        }
                    }
                }
            }
        }
    }
    return dsl
def search_scense_name_by_saletime(start_time, end_time):
    dsl = dsl_search_opentime(start_time, end_time)
    result = get_conn().search(dsl, index1, doc_type=document1)
    hits = result['hits']['hits']
    name_list = ''
    for hit in hits:
        name_list = hit['_source']['name'] + '，' + name_list
    return '售票时间在' + start_time + '到' + end_time + '之间的景区有' + name_list
def dsl_search_type(value):
    dsl = {
        "query": {
            "match": {
                "type": value
            }
        }
    }
    return dsl
def search_scense_name_by_type(type):
    dsl = dsl_search_type(type)
    result = get_conn().search(dsl, index1, doc_type=document1)
    hits = result['hits']['hits']
    name_list = ''
    for hit in hits:
        name_list = hit['_source']['name'] + '，' + name_list
    return '类型为' + type + '的景点有' + name_list
def dsl_search_history(value):
    dsl = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "hist": value
                        }
                    },
                    {
                        "match": {
                            "name": value
                        }
                    }
                ]
            }
        }
    }
    return dsl
def search_history_description_by_tag(tag):
    dsl = dsl_search_history(tag)
    result = get_conn().search(dsl, index2, doc_type=document2)
    hits = result['hits']['hits']
    hist_list = ''
    name_list = ''
    for hit in hits:
        for i in range(len(hit['_source']['hist'])):
            if tag in hit['_source']['hist'][i]:
                name_list += hit['_source']['name'] + '，'
                hist_list += hit['_source']['name'] + '景区的故事是' + str(hit['_source']['hist'][i]) + '；'
    return '关于' + tag + '的故事的景区有' + name_list + '其中，' + hist_list
def search_scense_id_by_name(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index1, doc_type=document1)
    return result['hits']['hits'][0]['_id']
def dsl_update_level(level):
    dsl = {
        "doc": {
            "level": level
        }
    }
    return dsl
def update_scense_level_by_id(name, level):
    dsl = dsl_update_level(level)
    get_conn().update(index=index1, doc_type=document1, body=dsl, id=search_scense_id_by_name(name))
def dsl_update_spot(spot):
    dsl = {
        "doc": {
            "spot": spot
        }
    }
    return dsl
def update_scense_spot_by_id(name, spot):
    dsl = dsl_update_spot(spot)
    get_conn().update(index=index1, doc_type=document1, body=dsl, id=search_scense_id_by_name(name))
def dsl_update_opentime(opent, closet):
    dsl = {
        "doc": {
            "opentime": [["opent", opent,], ["closet", closet]]
        }
    }
    return dsl
def update_scense_opentime_by_id(name, opent, closet):
    dsl = dsl_update_opentime(opent, closet)
    get_conn().update(index=index1, doc_type=document1, body=dsl, id=search_scense_id_by_name(name))
def dsl_update_saletime(startt, endt):
    dsl = {
        "doc": {
            "saletime": [["startt", startt,], ["endt", endt]]
        }
    }
    return dsl
def update_scense_saletime_by_id(name, startt, endt):
    dsl = dsl_update_saletime(startt, endt)
    get_conn().update(index=index1, doc_type=document1, body=dsl, id=search_scense_id_by_name(name))
def dsl_update_ticket(adult, student):
    dsl = {
        "doc": {
            "ticket": [["adult", adult,], ["student", student]]
        }
    }
    return dsl
def update_scense_ticket_by_id(name, adult, student):
    dsl = dsl_update_ticket(adult, student)
    get_conn().update(index=index1, doc_type=document1, body=dsl, id=search_scense_id_by_name(name))
def dsl_search_transport(value):
    dsl = {
        "query": {
            "match": {
                "transport": value
            }
        }
    }
    return dsl
def search_scense_name_by_transport(transport):
    dsl = dsl_search_transport(transport)
    result = get_conn().search(dsl, index1, doc_type=document1)
    hits = result['hits']['hits']
    name_list = ''
    for hit in hits:
        name_list = hit['_source']['name'] + '，' + name_list
    return '通过' + transport + '可到达的景点有' + name_list