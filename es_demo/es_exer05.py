import jieba
import pyhanlp
from elasticsearch import Elasticsearch
import jieba.posseg as pseg
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
# 获取属性名和对应的英文属性名parameter_list.txt
def get_parameter_list(filePath):
    with open(filePath,'r',encoding='utf-8') as f:
        pl = f.readlines()
        return pl

# def get_parameter(sentence):
#     parameter_list = []
#     jieba.load_userdict("../es_demo/vocabulary.txt")
#     # new_sentence = "/".join(jieba.posseg(sentence))
#     words = pseg.cut(sentence)
#     new_list = pyhanlp.HanLP.segment(sentence)
#     for i in range(len(new_list)):
#         if str(new_list[i]).endswith('/n') or str(new_list[i]).endswith('/ns'):
#             pl = get_parameter_list('parameter_list.txt')
#             for k in range(len(pl)):
#                 if str(new_list[i]).split('/')[0] in pl[k]:
#                     parameter_name = pl[k].split(' ')[1].replace('\n','')
#                     parameter_list.append(parameter_name)
#                     for j in range(i+1, len(new_list)):
#                         if str(new_list[j]).endswith('/n') or str(new_list[j]).endswith('/ns') or str(new_list[j]).endswith('/m'):
#                             parameter_list.append(str(new_list[j]).split('/')[0])
#                             if not str(new_list[j+1]).endswith('/n') and not str(new_list[j+1]).endswith('/ns') and not str(new_list[j+1]).endswith('/m'):
#                                 break
#                     break
#                 # if str(new_list[i]).split('/')[0] == '级别' or str(new_list[i]).split('/')[0] == '等级':
#                 #     parameter_list.append('level')
#                 #     for j in range(i+1, len(new_list)-1):
#                 #         if str(new_list[j]).endswith('/m') and str(new_list[j+1]).endswith('/nx'):
#                 #             parameter_list.append(str(new_list[j]).split('/')[0]+str(new_list[j+1]).split('/')[0])
#                 #             break
#     return parameter_list

# 获取问句中已知的属性名和属性值，以及要查询的属性名
def get_parameter(sentence):
    parameter_list = [] # 存储问句中对应的属性名
    jieba.load_userdict("../es_demo/vocabulary.txt") # 记载用户自定义词典，用于存放固有名词和希望识别到的属性名
    words = pseg.cut(sentence) # 对问句进行词性标注
    word = [] # 存放问句的分词
    flag = [] # 存放问句的词对应的词性
    parameter_name_num = 0 # 问句中的属性名个数
    parameter_word_num = 0 # 问句中的属性值个数
    parameter_l = [] #存放属性名列表parameter_list.txt
    for w in words:
        word.append(w.word)
        flag.append(w.flag)
    pl = get_parameter_list('parameter_list.txt')
    for j in range(len(pl)):
        pll = pl[j].split(' ')[0].split(',')
        for p in range(len(pll)):
            parameter_l.append(pll[p])
    # 遍历整个问句
    for i in range(len(word)):
        # 如果当前的分词存在于存放属性名列表parameter_list.txt中
        for j in range(len(pl)):
            pll = pl[j].split(' ')[0].split(',')
            if word[i] in pll:
                # 则取对应的英文属性名称放入parameter_list，并且问句中的属性名个数加一
                parameter_list.append(pl[j].split(' ')[1].replace('\n',''))
                parameter_name_num += 1
                # 如果该词的下一个词的词性为名词，nr，数字，ns，并且该词不在属性名列表parameter_list.txt中，则认为是描述该属性的属性值，把该词放入parameter_list中，并且问句中的属性值个数加一
                for k in range(i+1, len(word)):
                    if (flag[k] == 'n' or flag[k] == 'nr' or flag[k] == 'm' or flag[k] == 'ns') and word[k] not in parameter_l:
                        # if word[k] not in parameter_l:
                        parameter_list.append(word[k])
                        parameter_word_num += 1
                        if not flag[k+1] == 'n' and not flag[k+1] == 'nr' and not flag[k+1] == 'm' or flag[k] == 'ns':
                            break
                        break
                break
                # break
    return parameter_list, parameter_name_num, parameter_word_num
# 获取问句中的逻辑关系，从而在查询时判断是must还是should
def get_logical_relationship(sentence):
    if '或者' in sentence or '或' in sentence or '要么' in sentence:
        logical_relationship = 'should'
    else:
        logical_relationship = 'must'
    return logical_relationship
# 仅对于“且”关系，根据问句中的参数列表，选择不同的查询语句
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
# 进行查询，返回结果
def dsl_resultcollection(sentence):
    logical_relationship = get_logical_relationship(sentence)
    parameter_list, parameter_name_num, parameter_word_num = get_parameter(sentence)
    search_parameter = [] # 存放问句中是需要查询的属性名
    search_parameter_num = parameter_name_num - parameter_word_num # 一般来说，属性名与属性值是一对一的关系，所以多出来的就是要查询的属性名的个数
    # 遍历问句中的参数列表，得到已知的参数名、已知的参数值和要查询的参数名
    for item in reversed(parameter_list):
        if search_parameter_num != 0:
            search_parameter.append(item)
            search_parameter_num -= 1
            parameter_list.remove(item)
    if logical_relationship == 'should':
        while len(parameter_list) < 10:
            parameter_list.append('')
        dsl = dsl_search_should(logical_relationship, parameter_list)
        result = get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for i in range(len(search_parameter)):
            for hit in hits:
                name_list = str(hit['_source'][search_parameter[i]]) + '，' + name_list
        print(name_list)
    elif logical_relationship == 'must':
        print(parameter_list)
        print(search_parameter)
        dsl = switch_func(logical_relationship,parameter_list)
        result = get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for i in range(len(search_parameter)):
            for hit in hits:
                name_list = str(hit['_source'][search_parameter[i]]) + '，' + name_list
        print(name_list)
sentence = '类型为森林的景点哪些，在哪里'
# new_list = pyhanlp.HanLP.segment(sentence)
# print(new_list)
# logical_relationship = get_logical_relationship(sentence)
# parameter_list = get_parameter(sentence)
# print(parameter_list)
dsl_resultcollection(sentence)
# dsl_result('景点灵隐寺的类型是什么')
# new_list = pyhanlp.HanLP.segment('类型为寺庙的景点有哪些')
# print(new_list)