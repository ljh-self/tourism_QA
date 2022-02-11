import logging
import os
import urllib.request
import re
import csv
import random
import requests
from bs4 import BeautifulSoup
from pinyin import get

url = 'https://hangzhou.cncn.com/jingdian/'
fileheader = ['name', 'ticket', 'transport', 'description']
# 打开网页
def open_url(url):
    # 代理ip列表
    proxy_list = ['219.138.58.114:3128', '61.135.217.7:80', '101.201.79.172:808', '122.114.31.177:808']
    # 用户代理列表
    user_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
                 'User-Agent:Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16']
    index = random.randint(0, 3)
    # 使用代理ip的必要函数
    proxy_support = urllib.request.ProxyHandler({'http': proxy_list[index]})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    # 添加用户代理
    opener.addheaders = [('User-Agent', user_list[index])]
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        return ""

def getContext(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    name = soup.select("div.head_city>div.city_top.dj_detail>strong>a")[0].get_text()
    # header_ticket = soup.select("div.type>div.top>p>b>a")[0].get_text().replace('：', '')
    # print(header_ticket)
    ticket = soup.select("div.type>div.top>div")[0].get_text()
    # print(ticket)
    header_transport = soup.select("div.type>div.top>p>b>a")[1].get_text().replace('：', '')
    # print(header_transport)
    transport = soup.select("div.type>div.top>div")[-1].get_text().replace('    ', '')
    # print(transport)
    header_introduction = soup.select("div.type>p>b")[0].get_text().replace('：', '')
    # print(header_introduction)
    introduction = soup.select("div.type>div")[1].get_text()
    # print(introduction)
    contents = []
    contents.append(name)
    contents.append(ticket)
    contents.append(transport)
    contents.append(introduction)
    return contents

# 保存信息
def save_contents(contents, writer):
    # 从contents中取出一个作品信息content,写入csv文件中
    writer.writerow(contents)


# 写入csv文件
def download(filename, pages):
    global fileheader
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        if not os.stat(filename).st_size > 0:
            # 把fileheader的内容写入csv文件中
            csv_writer.writerow(fileheader)

        page_url = url + str(pages) + '/profile'
        # 用find_contents函数爬取当前网页的作品信息
        contents = getContext(page_url)
        # 把contents的内容通过save_contents函数存入csv文件中
        save_contents(contents, csv_writer)
# 获取拼音
def get_pinyin(text):
    pinyin = get(text, format='strip')
    return pinyin

if __name__ == '__main__':
    fileheader = ['name', 'ticket', 'transport', 'description']
    url = 'https://hangzhou.cncn.com/jingdian/'
    download('test1.csv', 'xihu')