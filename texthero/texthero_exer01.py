
# import texthero as hero
# import pandas as pd

# s = pd.Series("打架123")
# s = hero.remove_digits(s)
# print(s)


import jieba
from jieba.analyse.textrank import UndirectWeightedGraph
# 基于textrank的关键词抽取
texttrank = jieba.analyse.textrank('杭州西湖级别为5A级景点', topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
print(texttrank)
# 基于tfidf的关键词抽取
key = jieba.analyse.extract_tags('杭州西湖级别为5A级景点', topK=3, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
print(key)