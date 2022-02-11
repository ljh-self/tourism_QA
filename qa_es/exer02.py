import logging
import pyhanlp
from pinyin import get
from question_classfication.classfication_exer01 import Question_classify
from question_classfication.data_process_exer01 import Question
from question_classfication.insert_to_es import insert_csv_to_es
from spider_csv import spider_hzscense_exer02, spider_hzdetails_exer03
answer = ''
spot = ''
i = 0
logging.basicConfig(level = logging.INFO,#控制台打印的日志级别
                    filename = 'myexer.log',
                    filemode = 'a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format = '%(asctime)s - %(levelname)s: %(message)s'#日志格式
                    )

def switch_func(item, url, pyname):
    switcher = {
        0: spider_hzdetails_exer03.getContext(url + pyname + '/profile')[1],
        1: spider_hzscense_exer02.getContext(url + pyname + '/')[3],
        2: spider_hzscense_exer02.getContext(url + pyname + '/')[2],
        3: spider_hzscense_exer02.getContext(url + pyname + '/')[1],
        4: spider_hzscense_exer02.getContext(url + pyname + '/')[4],
        7: spider_hzdetails_exer03.getContext(url + pyname + '/profile')[3],
        9: spider_hzdetails_exer03.getContext(url + pyname + '/profile')[2]
    }
    return switcher.get(item)

def getinfo_online(sentence):
    global i
    name = ''
    url = 'https://hangzhou.cncn.com/jingdian/'
    list = pyhanlp.HanLP.segment(sentence)
    for item in list:
        if str(item).endswith('/ns'):
            name = str(item).replace('/ns', '')
            break
    answer = Question().question_process(sentence)
    pyname = get(name, format='strip')
    if answer == '我也不清楚':
        i = Question_classify().predict(sentence)
        result = switch_func(i, url, pyname)
        logging.info('moduleId="getinfo_online", keyword="' + name + '"')
        update_online(sentence)
        return result
    else:
        return answer

def update_online(sentence):
    global i, spot
    name = ''
    list = pyhanlp.HanLP.segment(sentence)
    for item in list:
        if str(item).endswith('/ns'):
            name = str(item).replace('/ns', '')
            break
        else:
            name = str(spot)
    pyname = get(name, format='strip')
    if i == 0 or i == 7 or i == 9:
        spider_hzdetails_exer03.download('test1.csv', pyname)
        insert_csv_to_es('test1.csv', 'myexer02', 'exer02')
        logging.info('moduleId="insert_into_es_myexer02_exer02", keyword="' + name + '"')
    else:
        spider_hzscense_exer02.download('mytest.csv', pyname)
        insert_csv_to_es('mytest.csv', 'myexer01', 'exer01')
        logging.info('moduleId="insert_into_es_myexer01_exer01", keyword="' + name + '"')

def multiple_rounds(new_question):
    global spot, answer
    flag = True
    new_list = pyhanlp.HanLP.segment(new_question)
    for item in new_list:
        if str(item).endswith('/ns'):
            spot = str(item).split('/')[0]
            answer = getinfo_online(new_question)
            print(answer)
            flag = False
            break
        else:
            break
    if flag:
        new_question = str(spot) + new_question
        answer = getinfo_online(new_question)
        print(answer)
    return answer

if __name__ == '__main__':
    question = "灵隐寺在哪"
    multiple_rounds(question)
    question = "票价是多少"
    multiple_rounds(question)
    question = "西湖的地址是哪里"
    multiple_rounds(question)