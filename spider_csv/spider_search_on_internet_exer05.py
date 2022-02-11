import urllib.request
import jieba
from jieba.analyse.textrank import UndirectWeightedGraph
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from lxml import etree


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        return ""
def getHref(url):
    href_list = []
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    taghs = soup.find_all('h3')
    for h3 in taghs:
        href = h3.find('a').get('href')
        href_list.append(href)
    return href_list
def getHrefInfo(href_url):
    hrefinfo = []
    # html = getHTMLText(href_url)
    # soup = BeautifulSoup(html, "html.parser")
    # content_list = soup.select("div>div>div>div>div>div>div.lemma-catalog>div.catalog-list.column-4>ol>li.level1>span.text>a")
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = requests.get(href_url, headers=header)
    # 为了防止中文乱码，编码使用原网页编码
    url.raise_for_status()
    url.encoding = url.apparent_encoding
    bject = etree.HTML(url.text)
    head = bject.xpath('/html/head//meta[@name="description"]/@content')
    print(head)
    # print(content_list)
    return hrefinfo
def getNeedInfo(question):
    info = ''
    key = jieba.analyse.extract_tags(question, topK=3, withWeight=False)
    for item in key:
        info += str(item)
    return info
if __name__ == '__main__':
    info = getNeedInfo('周杰伦是谁')
    print(info)
    url = 'https://baike.baidu.com/search/word?word=' + urllib.parse.quote(info)
    print(url)
    getHrefInfo(url)
    # print(hrefinfo)
