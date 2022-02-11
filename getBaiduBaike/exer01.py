import urllib.request
import random
import requests
from bs4 import BeautifulSoup
from pinyin import get

url = 'https://www.baidu.com/'

fileheader = ['title', 'url']
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
# 获取URL信息
def getContext(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    list = soup.select("div>div>h3.t>a")
    contents_title = []
    contents_url = []
    for item in list:
        contents_title.append(item[0].get_text())
    return contents_title, contents_url

# 获取拼音
def get_pinyin(text):
    pinyin = get(text, format='strip')
    return pinyin
