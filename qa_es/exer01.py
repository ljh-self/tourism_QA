import pyhanlp
from pinyin import get
from question_classfication.classfication_exer01 import Question_classify
from question_classfication.data_process_exer01 import Question
from question_classfication.insert_to_es import insert_csv_to_es
from spider_csv import spider_hzscense_exer02, spider_hzdetails_exer03
from spider_csv.spider_hzscense_exer02 import download

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

if __name__ == '__main__':
    url = 'https://hangzhou.cncn.com/jingdian/'
    sentence = "去灵隐寺怎么走"
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
        print(result)
        if i == 0 or i == 7 or i == 9:
            spider_hzdetails_exer03.download('test1.csv', pyname)
            insert_csv_to_es('test1.csv', 'myexer02', 'exer02')
        else:
            spider_hzscense_exer02.download('mytest.csv', pyname)
            insert_csv_to_es('mytest.csv', 'myexer01', 'exer01')
        answer = Question().question_process(sentence)
        while answer == '我也不清楚':
            answer = Question().question_process(sentence)
    print(answer)

