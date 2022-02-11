import csv
from datetime import datetime
import time
import sys
import wave
import jieba
import pyaudio
from aip import AipSpeech
from elasticsearch import Elasticsearch, helpers
from playsound import playsound
import os

APP_ID = '18409120'
API_KEY = 'Arbr32LAWUnOpfVwHN3CcqmA'
SECRET_KEY = '04lTe4bPgBiwCgLTHUO0neAwkR5cWrOE'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
index = 1
WAVE_OUTPUT_FILENAME = "./"+ str(index) +".wav"
process = ''
index_answer = 1
index_question = 1
subject = ''
pre_question = ''
fileheader = ['name','content']
contents = []
answer = ''
index = 'hzlm'
document = 'hzlmexer01'
def get_conn():
    es = Elasticsearch(hosts="119.3.65.142", http_auth=('elastic', 'elasticpwd'), port=9200, timeout=200)
    return es

def dsl_search_name(value):
    dsl = {
        "query": {
            "match": {
                "name": value
            }
        }
    }
    return dsl

def search_result(name):
    dsl = dsl_search_name(name)
    result = get_conn().search(dsl, index, doc_type=document)
    try:
        content = result['hits']['hits'][0]['_source']['content']
    except:
        content = '我还不清楚'
    return str(content)

def insert_csv_to_es(csvFile, index, doc_type):
    with open(csvFile, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(get_conn(), reader, index=index, doc_type=doc_type)

def save_contents(contents, writer):
    writer.writerow(contents)

def download(filename):
    global fileheader, contents
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        if not os.stat(filename).st_size > 0:
            csv_writer.writerow(fileheader)
        save_contents(contents, csv_writer)

def teach_to_robot(question, next_talk):
    global contents, answer
    contents = []
    if answer == '我还不清楚':
        if '答案是' in next_talk:
            answer = next_talk.replace('答案是','')
            question = question
            contents.append(question)
            contents.append(answer)
            download('teach.csv')
            insert_csv_to_es('teach.csv', index, document)

def print_one_by_one(text):
    sys.stdout.write("\r " + " " * 60 + "\r") # /r 光标回到行首
    sys.stdout.flush() #把缓冲区全部输出
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.1)

def wordtovoice(text,filepathin,filepathout):
    global result_answer
    with open(filepathin, 'w+', encoding='utf-8') as f:
        f.write(text)
    f.close()
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    infile = open(filepathin, encoding='utf-8')
    answer = str(infile.readlines()).replace(r'\n', '。')
    # 语音合成
    try:
        result_answer = client.synthesis(answer, 'zh', 1, {
            'vol': 5,
        })
    except Exception as e:
        print(e)

    # 语音写入
    if not isinstance(result_answer, dict):
        with open(filepathout, 'wb') as f:
            f.write(result_answer)
    f.close()
    infile.close()
    # 语音播放
    playsound(filepathout)

def record_content():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME

def voicetoword():
    global process, pre_question
    global index
    global index_question,index_answer
    # 语音录制
    filePath = record_content()
    # 语音识别
    result = client.asr(get_file_content(filePath), 'wav', 16000, {
    'dev_pid': 1536,
    })
    err_no = result['err_no']
    err_time = datetime.now()
    if err_no == 0:
        process = result['result'][0]
        # pre_question = process
        filepathin = "./txt/a" + str(index_question) + ".txt"
        index_question += 1
        with open(filepathin, 'w+', encoding='utf-8') as f:
            f.write(process)
    elif err_no == 3307:
        time_wait = err_time - time_pre
        if time_wait.seconds > 15:
            process = '您还在吗'
            filepathin = "./txt/a" + str(index_question) + ".txt"
            filepathout = "./mp3/question" + str(index_question) + ".mp3"
            index_question += 1
            wordtovoice(process,filepathin,filepathout)
            voicetoword()
        else:
            voicetoword()
    elif err_no == 3310:
        process = '您说的太长了，我记不住'
        filepathin = "./txt/a" + str(index_question) + ".txt"
        filepathout = "./mp3/question" + str(index_question) + ".mp3"
        index_question += 1
        wordtovoice(process, filepathin, filepathout)
    elif err_no == 3315:
        process = '语音服务器处理异常'
        filepathin = "./txt/a" + str(index_question) + ".txt"
        filepathout = "./mp3/question" + str(index_question) + ".mp3"
        index_question += 1
        wordtovoice(process, filepathin, filepathout)
    elif err_no == 3304:
        process = '用户请求超时'
        filepathin = "./txt/a" + str(index_question) + ".txt"
        filepathout = "./mp3/question" + str(index_question) + ".mp3"
        index_question += 1
        wordtovoice(process, filepathin, filepathout)
    else:
        process = '问题太多了，我理解不了'
        filepathin = "./txt/a" + str(index_question) + ".txt"
        filepathout = "./mp3/question" + str(index_question) + ".mp3"
        index_question += 1
        wordtovoice(process, filepathin, filepathout)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_file_content_question(filePath):
    with open(filePath, 'r') as f:
        return f.read()

def multiple_rounds(new_question):
    global answer, process, pre_question
    if '答案是' in new_question:
        teach_to_robot(pre_question, new_question)
        answer = '好的'
        print(answer)
        return answer
        # answer = Question().question_process(new_question)
    else:
        answer = search_result(new_question)
        print(answer)
        return answer

def chuli():
    global index
    global index_answer
    global index_question
    global flag
    global process
    global pre_question

    voicetoword()

    stop = ['呀','吗','，']
    sd = jieba.cut(process, cut_all=False)
    final = ''
    for seg in sd:
        # 去停用词
        if seg not in stop:
            final += seg
    process = final

    list = ['谢谢','不客气','你好','你好','再见','拜拜','小智','在呢']
    res = ''
    if process in list:
        for i in range(len(list)):
            if process == list[i]:
                res += list[i+1]
                print(res)
                filepathin = "./txt/a" + str(index_answer) + ".txt"
                filepathout = "./mp3/answer" + str(index_answer) + ".mp3"
                index_answer += 1
                wordtovoice(res,filepathin,filepathout)
                if process == "小智再见":
                    flag = False
                    break
                else:
                    flag = True
                    break
    elif flag == True :
        filepathin = "./txt/a" + str(index_answer) + ".txt"
        filepathout = "./mp3/answer" + str(index_answer) + ".mp3"
        index_answer += 1
        res = multiple_rounds(process)
        wordtovoice(res, filepathin, filepathout)
        pre_question = process

if __name__ == '__main__':
    a1 = "您好，请问您需要什么帮助？"
    print(a1)
    wordtovoice(a1,'./txt/0.txt','./mp3/0.mp3')
    time_pre = datetime.now()
    flag = True
    while (flag):
        chuli()