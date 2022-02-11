from elasticsearch import Elasticsearch

# es中的索引名称
index = 'hzlm'
document = 'hzlmexer01'

class QuestionTemplate():

    def __init__(self, question, word, flag):
        self.raw_question = question
        self.question_word = word
        self.question_flag = flag
        self.q_template_dict={
            0:self.search_result('产品背景'),
            1:self.search_result('产品特色'),
            2:self.search_result('一码到人'),
            3:self.search_result('一码归集'),
            4:self.search_result('一码互联'),
            5:self.search_result('一码替证'),
            6:self.search_result('扫码通行'),
            7:self.search_result('在线打卡'),
            8:self.search_result('产品功能'),
            9: self.search_result('用户登录'),
            10: self.search_result('实名认证'),
            11: self.search_result('系统首页'),
            12: self.search_result('家庭成员管理'),
            13: self.search_result('每日健康打卡'),
            14: self.search_result('疫情线索上报'),
            15: self.search_result('执行人员使用')
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
        answer = self.q_template_dict[template_id]
        return answer

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

    def search_result(self, name):
        dsl = self.dsl_search_name(name)
        result = self.get_conn().search(dsl, index, doc_type=document)
        content = result['hits']['hits'][0]['_source']['content']
        return name + str(content)

