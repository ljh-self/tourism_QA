import math

def idf(corpus):
    idfs = {}
    d = 0.0
    # 统计词出现次数
    for doc in corpus:
        d += 1
        counted = []
        for word in doc:
            if not word in counted:
                counted.append(word)
                if word in idfs:
                    idfs[word] += 1
                else:
                    idfs[word] = 1
    # 计算每个词逆文档值
    for word in idfs:
        idfs[word] = math.log(d / float(idfs[word]))
    return idfs

if __name__ == '__main__':
    # 获取需要的语料库，根据实际情况自行更改
    # 这里获取的语料库是每个文档的分词结果列表的列表
    corpus = getCorpus()
    idfs = idf(corpus)
    for doc in corpus:
        tfidfs = {}
        for word in doc:
            if word in tfs:
                tfidfs[word] += 1
            else:
                tfidfs[word] = 1
        for word in tfidfs:
            tfidfs[word] *= idfs[word]