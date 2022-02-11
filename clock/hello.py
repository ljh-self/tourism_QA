import wave
import time

import pyaudio
from aip import AipSpeech
from playsound import playsound

APP_ID = '18409120'
API_KEY = 'Arbr32LAWUnOpfVwHN3CcqmA'
SECRET_KEY = '04lTe4bPgBiwCgLTHUO0neAwkR5cWrOE'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "./"+ str(1) +".wav"

index_question = 1

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

if __name__ == '__main__':
    # question = '欢迎您选乘星空联盟成员，中国国际航空公司8638航班，前往萧山国际机场。'
    # filepathin = str(index_question) + ".txt"
    # filepathout = str(index_question) + ".mp3"
    # wordtovoice(question, filepathin, filepathout)
    #
    time.sleep(2)
    # question = '你好'
    question = '你好'
    filepathin = str(index_question) + ".txt"
    filepathout = str(index_question) + ".mp3"
    wordtovoice(question, filepathin, filepathout)
    index_question = 2

    time.sleep(3)
    # question = '杭州西湖是什么级别的景区'
    question = '杭州西湖被评为“国家AAAAA级旅游景区”。'
    filepathin = str(index_question) + ".txt"
    filepathout = str(index_question) + ".mp3"
    wordtovoice(question, filepathin, filepathout)
    index_question = 3

    time.sleep(3)
    # question = '杭州西湖有哪些景观'
    question = '杭州西湖景区有苏堤春晓、雷峰夕照、三潭印月、南屏晚钟、断桥残雪等景观。'
    filepathin = str(index_question) + ".txt"
    filepathout = str(index_question) + ".mp3"
    wordtovoice(question, filepathin, filepathout)

    time.sleep(3)
    index_question = 4
    # question = '如何评价杭州西湖'
    question = '苏东坡的名句“欲把西湖比西子，浓妆淡抹总相宜”，让人任何时候提到杭州，西湖都是一个绕不开的词。山水与文化在杭州完成了最佳的叠合，杭州也因西湖成为中国城市与自然结合最完美的都市。'
    filepathin = str(index_question) + ".txt"
    filepathout = str(index_question) + ".mp3"
    wordtovoice(question, filepathin, filepathout)

