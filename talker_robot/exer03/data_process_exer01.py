'''
接收原始问题
对原始问题进行分词、词性标注等处理
对问题进行抽象
'''
import pyhanlp
from talker_robot.exer03.classfication_exer01 import Question_classify
from talker_robot.exer03.question_template import QuestionTemplate
import sys, os

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

class Question():
    def __init__(self):
        # 初始化相关设置：读取词汇表，训练分类器，连接数据库
        self.init_config()

    def init_config(self):
        # 读取词汇表
        # with(open("../question_classfication/data_question/vocabulary.txt","r",encoding="utf-8")) as fr:
        with(open("./question_type/vocabulary.txt", "r", encoding="utf-8")) as fr:
            vocab_list=fr.readlines()
        vocab_dict={}
        vocablist=[]
        for one in vocab_list:
            word_id,word=str(one).strip().split(":")
            vocab_dict[str(word).strip()]=int(word_id)
            vocablist.append(str(word).strip())
        # print(vocab_dict)
        self.vocab=vocab_dict

        # 训练分类器
        self.classify_model=Question_classify()
        # 读取问题模板
        # with(open("../question_classfication/data_question/classfication.txt","r",encoding="utf-8")) as f:
        with(open("./question_type/classfication.txt", "r", encoding="utf-8")) as f:
            question_mode_list=f.readlines()
        self.question_mode_dict={}
        for one_mode in question_mode_list:
            # 读取一行
            mode_id,mode_str=str(one_mode).strip().split(":")
            # 处理一行，并存入
            self.question_mode_dict[int(mode_id)]=str(mode_str).strip()
        # print(self.question_mode_dict)

        # # 创建问题模板对象
        # self.questiontemplate = QuestionTemplate()

    def question_process(self,question):
        # 接收问题
        self.raw_question=str(question).strip()
        # print(self.raw_question)
        # 对问题进行词性标注
        self.pos_quesiton=self.question_posseg()
        # print(self.pos_quesiton)
        # 创建问题模板对象
        self.questiontemplate = QuestionTemplate(self.raw_question,self.question_word,self.question_flag)
        # 得到问题的模板
        self.question_template_id_str=self.get_question_template()
        # print(self.question_template_id_str)
        # 查询图数据库,得到答案
        self.answer=self.query_template()
        return(self.answer)

    def question_posseg(self):
        question_seged = pyhanlp.HanLP.segment(self.raw_question)
        result=[]
        result.append(question_seged)
        result = question_seged
        question_word, question_flag = [], []
        for item in question_seged:
            s = str(item)
            question_word.append(s.split('/')[0].strip())
            question_flag.append(s.split('/')[1].strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        return result

    def get_question_template(self):
        # 抽象问题
        for item in ['n']:
            while (item in self.question_flag):
                ix=self.question_flag.index(item)
                self.question_word[ix]=item
                self.question_flag[ix]=item+"ed"
        # 将问题转化字符串
        str_question="".join(self.question_word)
        # print("抽象问题为：",str_question)
        # 通过分类器获取问题模板编号
        question_template_num=self.classify_model.predict(str_question)
        # print("使用模板编号：",question_template_num)
        question_template=self.question_mode_dict[question_template_num]
        # print("问题模板：",question_template)
        question_template_id_str=str(question_template_num)+"\t"+question_template
        return question_template_id_str

    # 根据问题模板的具体类容，构造查询语句，并查询
    def query_template(self):
        # 调用问题模板类中的获取答案的方法
        try:
            answer=self.questiontemplate.get_question_answer(self.pos_quesiton,self.question_template_id_str)
        except:
            answer="我也不清楚"
        # answer = self.questiontemplate.get_question_answer(self.pos_quesiton, self.question_template_id_str)
        return answer
