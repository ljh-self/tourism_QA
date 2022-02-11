import csv
import logging
import re
from elasticsearch import helpers,Elasticsearch

# es中的索引名称
# index1 = 'hzscense'
# index2 = 'hzhistory'
# es中的文档名称
# document1 = 'scense'
# document2 = 'history'
index1 = 'myexer01'
document1 = 'exer01'
index2 = 'myexer02'
document2 = 'exer02'

class QuestionTemplate():

    def __init__(self, question, word, flag):
        self.raw_question = question
        self.question_word = word
        self.question_flag = flag
        self.q_template_dict={
            0:self.search_scense_ticket_by_name,
            1:self.search_scense_type_by_name,
            2:self.search_scense_address_by_name,
            3:self.search_scense_level_by_name,
            4:self.search_scense_opentime_by_name,
            5:self.search_scense_name_by_level,
            6:self.search_scense_name_by_opentime,
            7:self.search_scense_description_by_name,
            8:self.search_scense_name_by_type,
            9:self.search_scense_transport_by_name
        }

    def get_question_answer(self, question, template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t")) == 2
        template_id,template_str = int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id = template_id
        self.template_str2list = str(template_str).split()

        question_word, question_flag = [], []
        for item in question:
            s = str(item)
            question_word.append(s.split('/')[0].strip())
            question_flag.append(s.split('/')[1].strip())
        self.raw_question = question
        self.question_word = question_word
        self.question_flag = question_flag

        assert len(question_flag) == len(question_word)
        # 根据问题模板来做对应的处理，获取答案
        answer = self.q_template_dict[template_id]()
        return answer

    def get_scense_name(self):
        tag_index = self.question_flag.index("ns")
        name = self.question_word[tag_index]
        return name

    def get_scense_level(self):
        tag_index = self.question_flag.index("m")
        level = self.question_word[tag_index]
        return level

    def get_name(self, type_str):
        name_count=self.question_flag.count(type_str)
        if name_count==1:
            ## 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            ## 获取电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list=[]
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    def get_num_x(self):
        x = re.sub(r'\D', "", "".join(self.question_word))
        return x

    # 获取es连接
    def get_conn(self):
        es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
        return es

    def dsl_search_name(self, value):
        dsl = {
            "query": {
                "match": {
                    "name": value
                }
            }
        }
        return dsl

    def search_scense_ticket_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index2, doc_type=document2)
        ticket = result['hits']['hits'][0]['_source']['ticket']
        # return name + '景区成人票价为' + ticket.get('adult') + '每人，' + '学生票价为' + ticket.get('student') + '每人。'
        logging.info('moduleId="search_scense_ticket_by_name", keyword="' + name + '"')
        return name + '景区票价为' + ticket

    def search_scense_type_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        type = result['hits']['hits'][0]['_source']['type']
        logging.info('moduleId="search_scense_type_by_name", keyword="' + name + '"')
        return name + '景区的类型为' + str(type)

    def search_scense_address_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        address = result['hits']['hits'][0]['_source']['address']
        logging.info('moduleId="search_scense_address_by_name", keyword="' + name + '"')
        return name + '景区的地址为' + address

    def search_scense_level_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        level = result['hits']['hits'][0]['_source']['level']
        logging.info('moduleId="search_scense_level_by_name", keyword="' + name + '"')
        return name + '景区的级别为' + level + '级'

    def search_scense_spot_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        spot = result['hits']['hits'][0]['_source']['spot']
        logging.info('moduleId="search_scense_spot_by_name", keyword="' + name + '"')
        return name + '景区中有' + spot

    def search_scense_opentime_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        opentime = result['hits']['hits'][0]['_source']['opentime']
        logging.info('moduleId="search_scense_opentime_by_name", keyword="' + name + '"')
        return name + '景区开放时间为' + opentime

    def search_scense_transport_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index2, doc_type=document2)
        transport = result['hits']['hits'][0]['_source']['transport']
        logging.info('moduleId="search_scense_transport_by_name", keyword="' + name + '"')
        return transport

    def search_scense_description_by_name(self):
        name = self.get_scense_name()
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index2, doc_type=document2)
        description = result['hits']['hits'][0]['_source']['description']
        logging.info('moduleId="search_scense_description_by_name", keyword="' + name + '"')
        return description
    def dsl_search_level(self, value):
        dsl = {
            "query": {
                "match": {
                    "level": value
                }
            }
        }
        return dsl
    def search_scense_name_by_level(self):
        level = self.get_scense_level()
        dsl = self.dsl_search_level(str(level)+'A')
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for hit in hits:
            name_list = hit['_source']['name'] + '，' + name_list
        logging.info('moduleId="search_scense_name_by_level", keyword="' + level + 'A"')
        return '级别为' + level + '级的景区有' + name_list

    def dsl_search_opentime(self, value1, value2):
        dsl = {
            "query": {
                "bool": {
                    "must": [
                        {
                          "range": {
                            "opentime": {
                                "lte": value1

                            }
                          }
                        },
                        {
                          "range": {
                            "closetime": {
                              "gte": value2
                            }
                          }
                        }
                    ]
                }
            }
        }
        return dsl

    def search_scense_name_by_opentime(self):
        open_time = self.get_name("m")[0]
        close_time = self.get_name("m")[1]
        dsl = self.dsl_search_opentime(open_time, close_time)
        print(dsl)
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        print(result)
        hits = result['hits']['hits']
        name_list = ''
        for hit in hits:
            name_list = hit['_source']['name'] + '，' + name_list
        logging.info('moduleId="search_scense_name_by_opentime", keyword="' + open_time + '"')
        return '开放时间在' + open_time + '到' + close_time + '之间的景区有' + name_list

    def dsl_search_type(self, value):
        dsl = {
            "query": {
                "match": {
                    "type": value
                }
            }
        }
        return dsl

    def search_scense_name_by_type(self):
        type = self.get_name("n")[1:-1]
        dsl = self.dsl_search_type(str(type))
        result = self.get_conn().search(dsl, index1, doc_type=document1)
        hits = result['hits']['hits']
        name_list = ''
        for hit in hits:
            name_list = hit['_source']['name'] + '，' + name_list
        logging.info('moduleId="search_scense_name_by_type", keyword="' + str(type) + '"')
        return '类型为' + str(type) + '的景点有' + name_list
