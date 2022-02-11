import sys
import time
import subprocess

#实现闹钟功能
def alert(sentence):
    set_time = sentence
    # set_time = input("设置闹钟时间: ")
    print(f'闹钟设置为: {set_time}')
    while True:
        t = time.localtime()
        fmt = "%H:%M:%S"
        now = time.strftime(fmt,t)
        sys.stdout.write(now + '\r')
        sys.stdout.flush()
        time.sleep(1)

        if now[:5] == set_time.rjust(5,'0'):
            print('起床了')
            # subprocess.Popen(['start','C:/Users/RCP/Music/打出名堂.mp3'],shell=True)
            break

if __name__ == "__main__":
    sentence = '我要定明天8点的闹钟'
    alert()