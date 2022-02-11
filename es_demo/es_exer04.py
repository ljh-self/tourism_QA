import pyhanlp
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

def dsl_search_should(logical_relationship,parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship:[
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    },
                    {
                        "match": {
                            parameter_list[2]: parameter_list[3]
                        }
                    },
                    {
                        "match": {
                            parameter_list[4]: parameter_list[5]
                        }
                    },
                    {
                        "match": {
                            parameter_list[6]: parameter_list[7]
                        }
                    },
                    {
                        "match": {
                            parameter_list[8]: parameter_list[9]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def dsl_search_must1(logical_relationship, parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship: [
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def dsl_search_must2(logical_relationship, parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship: [
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    },
                    {
                        "match": {
                            parameter_list[2]: parameter_list[3]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def dsl_search_must3(logical_relationship, parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship: [
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    },
                    {
                        "match": {
                            parameter_list[2]: parameter_list[3]
                        }
                    },
                    {
                        "match": {
                            parameter_list[4]: parameter_list[5]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def dsl_search_must4(logical_relationship, parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship: [
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    },
                    {
                        "match": {
                            parameter_list[2]: parameter_list[3]
                        }
                    },
                    {
                        "match": {
                            parameter_list[4]: parameter_list[5]
                        }
                    },
                    {
                        "match": {
                            parameter_list[6]: parameter_list[7]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def dsl_search_must5(logical_relationship, parameter_list):
    dsl = {
        "query": {
            "bool": {
                logical_relationship: [
                    {
                        "match": {
                            parameter_list[0]: parameter_list[1]
                        }
                    },
                    {
                        "match": {
                            parameter_list[2]: parameter_list[3]
                        }
                    },
                    {
                        "match": {
                            parameter_list[4]: parameter_list[5]
                        }
                    },
                    {
                        "match": {
                            parameter_list[6]: parameter_list[7]
                        }
                    },
                    {
                        "match": {
                            parameter_list[8]: parameter_list[9]
                        }
                    }
                ]
            }
        }
    }
    return dsl
def get_parameter(sentence):
    parameter_list = []
    new_list = pyhanlp.HanLP.segment(sentence)
    for i in range(len(new_list)-2):
        if str(new_list[i]).endswith('/n'):
            if str(new_list[i]).split('/')[0] == '类型' or str(new_list[i]).split('/')[0] == '类别' or str(new_list[i]).split('/')[0] == '样式' or str(new_list[i]).split('/')[0] == '种类':
                parameter_list.append('type')
                for j in range(i+1, len(new_list)-1):
                    if str(new_list[j]).endswith('/n'):
                        parameter_list.append(str(new_list[j]).split('/')[0])
                        if not str(new_list[j+1]).endswith('/n'):
                            break
                break
            if str(new_list[i]).split('/')[0] == '级别' or str(new_list[i]).split('/')[0] == '等级':
                parameter_list.append('level')
                for j in range(i+1, len(new_list)-1):
                    if str(new_list[j]).endswith('/m') and str(new_list[j+1]).endswith('/nx'):
                        parameter_list.append(str(new_list[j]).split('/')[0]+str(new_list[j+1]).split('/')[0])
                        break
    return parameter_list
def get_logical_relationship(sentence):
    if '或者' in sentence or '或' in sentence or '要么' in sentence:
        logical_relationship = 'should'
    else:
        logical_relationship = 'must'
    return logical_relationship
def switch_func(logical_relationship, parameter_list):
    if len(parameter_list) == 2:
        return dsl_search_must1(logical_relationship, parameter_list)
    if len(parameter_list) == 4:
        return dsl_search_must2(logical_relationship, parameter_list)
    if len(parameter_list) == 6:
        return dsl_search_must3(logical_relationship, parameter_list)
    if len(parameter_list) == 8:
        return dsl_search_must4(logical_relationship, parameter_list)
    if len(parameter_list) == 10:
        return dsl_search_must5(logical_relationship, parameter_list)
def dsl_resultcollection(logical_relationship, parameter_list):
    if logical_relationship == 'should':
        while len(parameter_list) < 10:
            parameter_list.append('')
        dsl = dsl_search_should(logical_relationship, parameter_list)
        result = get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for hit in hits:
            name_list = hit['_source']['name'] + '，' + name_list
        print(name_list)
    elif logical_relationship == 'must':
        dsl = switch_func(logical_relationship,parameter_list)
        result = get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for hit in hits:
            name_list = hit['_source']['name'] + '，' + name_list
        print(name_list)
sentence = '类型是寺庙的景点有哪些'
# new_list = pyhanlp.HanLP.segment(sentence)
# print(new_list)
logical_relationship = get_logical_relationship(sentence)
parameter_list = get_parameter(sentence)
# print(parameter_list)
dsl_resultcollection(logical_relationship, parameter_list)