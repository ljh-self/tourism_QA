from elasticsearch import Elasticsearch
# 连接es
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es
# # 查询数据
# result = es.search(index='ljh', doc_type='user', ignore=400)
# # 通过hits进行查询结果的遍历
# value = result['hits']['hits']
# for va in value:
#     print(va['_source']['name'])
#
def tags_search(es, name, cls):
    dsl = {
        'query': {
            "bool": {
                "should": [
                    {
                    'match': {
                        'name': name
                        }
                    },{
                    "match": {
                        'cls': cls
                        }
                    }
                ]
            }
        }
    }
    return es.search(index='ljh', doc_type='user', body=dsl)

result = tags_search(get_conn(),'张三', '计算机')
value = result['hits']['hits'][0]
print(value)
for va in value:
    print(va['_source']['name'])
es = get_conn()
# 新建数据表
result = es.indices.create(index='ljh', doc_type='user', ignore=400)
print(result)

# 插入数据
data = {'title': '美国留给伊拉克的是个烂摊子吗', 'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm'}
# 方法一：create()方法需要指定id字段
result = es.create(index='news', doc_type='politics', id=1, body=data)
print(result)
# 方法二：index()方法实际上是对create()方法的封装，但是不用指定id字段，系统会自动为其分配id
result = es.index(index='news', doc_type='politics', body=data)
print(result)

# 删除数据
result = es.delete(index='news', doc_type='politics', id=1)
print(result)

# 更新数据
def data_update(x):
    data = {
        "doc": {
            "age": x
        }
    }
    es.update(index='ljh', doc_type='user', body=data, id=1)
    # print(result)
data_update(24)
# 查询数据
result = es.search(index='ljh', doc_type='user', ignore=400)
# 通过hits进行查询结果的遍历
value = result['hits']['hits']
for va in value:
    print(va['_source']['age'])