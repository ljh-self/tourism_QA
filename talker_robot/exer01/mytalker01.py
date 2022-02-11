from datetime import datetime
import time
import sys
import wave
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
index = 1
WAVE_OUTPUT_FILENAME = "./"+ str(index) +".wav"
process = ''

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
    global process
    global index
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
        print(process)
    elif err_no == 3307:
        time_wait = err_time - time_pre
        if time_wait.seconds > 20:
            process = '您还在吗'
            wordtovoice(process,filepathin='./2.txt',filepathout='./3.mp3')
        else:
            voicetoword()
    elif err_no == 3310:
        process = '您说的太长了，我记不住'
        wordtovoice(process, filepathin='./2.txt', filepathout='./3.mp3')
    elif err_no == 3315:
        process = '语音服务器处理异常'
        wordtovoice(process, filepathin='./2.txt', filepathout='./3.wav')
    elif err_no == 3304:
        process = '用户请求超时'
        wordtovoice(process, filepathin='./2.txt', filepathout='./3.wav')
    else:
        process = '问题太多了，我理解不了'
        wordtovoice(process, filepathin='./2.txt', filepathout='./3.wav')

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

if __name__ == '__main__':
    a1 = "您好，请问您需要什么帮助？"
    time_pre = datetime.now()
    print(a1)
    wordtovoice(a1,'./4.txt','./5.mp3')
    voicetoword()