

from mytest.test01.query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0:self.get_ticket,
            1:self.get_type,
            2:self.get_address,
            3:self.get_level,
            4:self.get_opentime,
            5:self.get_introduction
        }

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        return answer

    # 获取景点名字
    def get_spot_name(self):
        ## 获取ns在原问题中的下标
        tag_index = self.question_flag.index("ns")
        ## 获取景点名称
        spot_name = self.question_word[tag_index]
        return spot_name
    # 获取类别
    def get_name(self,type_str):
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
    # 0:ns 票价
    def get_ticket(self):
        # 获取电影名称，这个是在原问题中抽取的
        spot_name=self.get_spot_name()
        cql = f"match (p:Place)-[]->() where p.title='{spot_name}' return p.price"
        print(cql)
        answer = self.graph.run(cql)[0]
        # print(answer)
        answer = round(answer, 2)
        final_answer=spot_name+"景点票价为"+str(answer)
        return final_answer
    # 1:ns 类型
    def get_type(self):
        spot_name = self.get_spot_name()
        cql = f"match (p:Place)-[]->() where p.title='{spot_name}' return p.type"
        print(cql)
        answer = self.graph.run(cql)
        answer_set = set(answer)
        answer_list = list(answer_set)
        answer = "、".join(answer_list)
        final_answer = spot_name + "是" + str(answer) + "等类型的景点"
        return final_answer
    # 2:ns 地址
    def get_address(self):
        spot_name = self.get_spot_name()
        cql = f"match(p:Place)-[r:locatedin]->(b) where p.title='{spot_name}' return b.address"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = spot_name + "在" + str(answer)
        return final_answer
    # 3:ns 简介
    def get_introduction(self):
        spot_name = self.get_spot_name()
        cql = f"match(p:Place)-[]->() where p.title='{spot_name}' return p.introduction"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = str(answer)
        return final_answer
    # 4:ns 等级
    def get_level(self):
        spot_name=self.get_spot_name()
        cql = f"match(p:Place)-[]->() where p.title='{spot_name}' return p.rating"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = spot_name + "的等级为" + str(answer)
        return final_answer
    # 5:ns 开放时间
    def get_opentime(self):
        spot_name = self.get_spot_name()
        cql = f"match(p:Place)-[]->() where p.title='{spot_name}' return p.opentime"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = spot_name + "的开放时间为" + str(answer)
        return final_answer
    # # 6:ns 交通
    # def get_transport(self):
    #     spot_name = self.get_spot_name()
    #     cql = f"match(s:Spot)-[]->() where s.name='{spot_name}' return s.transport"
    #     print(cql)
    #     answer = self.graph.run(cql)[0]
    #     final_answer = '到达' + spot_name + '景点的交通方式有' + answer
    #     return  final_answer
    # def get_typename_spot_list(self, type):
    #     cql = f"match(t:Type)-[]->(s:Spot) where t.name='{type}' return s.name"
    #     answer = self.graph.run(cql)
    #     answer_set = set(answer)
    #     answer_list = list(answer_set)
    #     return answer_list
    # # 7:类型 景点
    # def get_type_spot_name(self):
    #     type_list = self.get_name("n")
    #     spot_list = {}
    #     result_list = {}
    #     for i,type in enumerate(type_list):
    #         answer_list = self.get_typename_spot_list(type)
    #         spot_list[i] = answer_list
    #         result_list = list(set(spot_list[i]).intersection(set(result_list)))
    #     answer = "、".join(result_list)
    #     final_answer = "类型为" + type_list + "的景点有" + answer
    #     return final_answer
    # def get_levelname_spot_list(self, level):
    #     cql = f"match(l:Level)-[]->(s:Spot) where l.name='{level}' return s.name"
    #     answer = self.graph.run(cql)
    #     answer_set = set(answer)
    #     answer_list = list(answer_set)
    #     return answer_list
    # # 级别 景点
    # def get_level_spot_name(self):
    #     level = self.get_num_x()
    #     result_list = self.get_levelname_spot_list(level)
    #     answer = "、".join(result_list)
    #     final_answer = "级别为" + level + "的景点有" + answer
    #     return final_answer
    def get_score(self):
        spot_name = self.get_spot_name()
        cql = f"match(p:Place)-[]->() where p.title='{spot_name}' return p.rating"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = spot_name + '景点的评分为' + answer
        return final_answer