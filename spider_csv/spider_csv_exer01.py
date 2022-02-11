import urllib.request
import re
import csv
import random

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

# 运用正则表达式提出作品信息
def find_contents(url):
    html = open_url(url).decode('utf-8')

    # 编写正则表达式
    book_name = r'<a href=".*?" target="_blank" data-eid=".*?" data-bid="\d*?">(.*?)</a>'
    book_author = r'<a class="name" href=".*?" data-eid=".*?" target="_blank">(.*?)</a>'
    book_type1 = r'<a href=".*?" target="_blank" data-eid=".*?">(.*?)</a>'
    # 新增一个类型
    book_type2 = r'<a class="go-sub-type" data-typeid="\d*?" data-subtypeid="\d*?" href="javascript:" data-eid=".*?">(.*?)</a>'
    book_state = r'<span >(.*?)</span>'
    book_intro = r'<p class="intro">(.*?)</p>'

    informations = book_name + r'.*?' + book_author + r'.*?' + book_type1 + \
        r'.*?' + book_type2 + r'.*?' + book_state + r'.*?' + book_intro
    # 返回一个正则表达式对象
    reg = re.compile(informations, re.S)
    # 开始查找所有信息
    contents_list = re.findall(reg, html)
    contents = []

    # 遍历每一个作品信息，进行修改
    for content in contents_list:
        content = list(content)
        new_content = content[:2]
        new_content.append(content[2] + '-' + content[3])
        new_content.append(content[4])
        new_content.append(content[5].strip())
        contents.append(new_content)

    return contents

# 保存作品信息
def save_contents(contents, writer):
    # 从contents中取出一个作品信息content,写入csv文件中
    for content in contents:
        writer.writerow(content)


# 主函数
def download(filename, pages=1):
    # 这里是固定部分的URL
    url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page='

    fileheader = ['作品', '作者', '类型', '状态', '简介']
    with open(filename, 'w', newline='', encoding='gb18030') as f:
        csv_writer = csv.writer(f)
        # 把fileheader的内容写入csv文件中
        csv_writer.writerow(fileheader)

        # 开始遍历每个网页，爬取作品信息
        for page in range(1, pages + 1):
            page_url = url + str(page)
            # 用find_contents函数爬取当前网页的作品信息
            contents = find_contents(page_url)
            # 把contents的内容通过save_contents函数存入csv文件中
            save_contents(contents, csv_writer)


if __name__ == '__main__':
    download('mytest.csv', 2)

