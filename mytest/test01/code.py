import sys

from mytest.test01.preprocess_data import Question

urls = ('/', 'index','/add','add')

que = Question()

# 处理问题的方法
def dealquestion(question):
    # 查询知识图谱
    answer=que.question_process(question)
    # answer=12
    return answer
