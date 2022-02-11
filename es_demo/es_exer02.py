from elasticsearch import Elasticsearch
# es中的索引名称
index = 'ljh'
# es中的文档名称
document = 'user'

# 获取es连接
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
# 插入数据
def insert_data(name, age, cls, tags):
    dsl = {
        "name": name,
        "age": age,
        "cls": cls,
        "tags": tags
    }
    # 自动分配id
    get_conn().index(index=index, body=dsl, doc_type=document)
# 根据id对其所有信息进行更新
def update_data(name, age, cls, tags):
    dsl = {
        "doc": {
            "name": name,
            "age": age,
            "cls": cls,
            "tags": tags
        }
    }
    get_conn().update(index, search_id(name), dsl, doc_type=document)
def dsl_value(value):
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    return dsl
# 根据姓名获取id
def search_id(name):
    dsl = dsl_value(name)
    result = get_conn().search(dsl, index, doc_type=document)
    return result['hits']['hits'][0]['_id']
# 根据姓名获取年龄
def search_age(name):
    dsl = dsl_value(name)
    result = get_conn().search(dsl, index, doc_type=document)
    return result['hits']['hits'][0]['_source']['age']
# 根据姓名获取班级
def search_cls(name):
    dsl = dsl_value(name)
    result = get_conn().search(dsl, index, doc_type=document)
    return result['hits']['hits'][0]['_source']['cls']
# 根据姓名获取标签
def search_tags(name):
    dsl = dsl_value(name)
    result = get_conn().search(dsl, index, doc_type=document)
    return result['hits']['hits'][0]['_source']['tags']

# update_data('张三', '19', '计算机科学1班',['直男','计算机','打游戏'])
# insert_data('张三','23','计算机2班',['暖男','宅男','摩羯座'])
# insert_data('小明','20','计算机1班',['暖男','金牛座'])