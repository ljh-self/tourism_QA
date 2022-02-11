import requests
from lxml import etree
import jieba
from jieba import posseg
import re
allowRelationships = ['母亲','父亲','儿子','女儿','母','父','下嫁','又嫁','祖父','祖母','孙','孙子','改嫁','哥哥','姐姐','弟弟']
hraders={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}
url='http://www.uuqgs.com/lsrw/1358.html'
html = requests.get(url,headers=hraders)
text = html.content.decode("gb2312","ignore")
selector = etree.HTML(text)
content=selector.xpath('//div[@id="newscont"]/p/text()')
# 抽取的实体词性
allowTags = ['nr']
relationships = set()
for line in content:
    sentence = []
    for word, tag in posseg.cut(line):
        if tag == 'nr' or word in allowRelationships:
            sentence.append(word)
    sentence = ' '.join(sentence)
    sentenceSplit = sentence.split(' ')
    # print("原始文本：", line)
    print(sentenceSplit)
    for i in range(0,len(sentenceSplit)-1):
        if sentenceSplit[i] in allowRelationships:
            source = sentenceSplit[i-1]
            relationship = sentenceSplit[i]
            target = sentenceSplit[i+1]
            print('提取结果：',source+'->'+relationship+'->'+target)
            relationships.add(source+'->'+relationship+'->'+target)