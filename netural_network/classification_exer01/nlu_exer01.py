# use natural language toolkit
import nltk
import self
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import jpype
import pyhanlp
# tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
from hanlp import hanlp
from collections import OrderedDict
jvmPath = jpype.getDefaultJVMPath() # 获得系统的jvm路径
ext_classpath = r"F:/pycharm_pkgs/hanlp/hanlp-1.7.8-release/hanlp-1.7.8.jar;F:/pycharm_pkgs/hanlp/hanlp-1.7.8-release/hanlp-1.7.8-sources.jar;F:/pycharm_pkgs/hanlp/data"
jvmArg = '-Djava.class.path=' + ext_classpath
try:
    jpype.startJVM(jvmPath, jvmArg, "-Xms512m", "-Xmx512m")
except:
    pass
def TraditionalChinese2SimplifiedChinese(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    return HanLP.convertToSimplifiedChinese(sentence_str)
training_data = []
training_data.append({"class":"地址", "sentence":"地址是哪里?"})
training_data.append({"class":"地址", "sentence":"在哪?"})
training_data.append({"class":"地址", "sentence":"地址在哪里"})
training_data.append({"class":"地址", "sentence":"在什么地方?"})

training_data.append({"class":"票价", "sentence":"票价是多少"})
training_data.append({"class":"票价", "sentence":"需要多少钱"})
training_data.append({"class":"票价", "sentence":"门票多少钱"})
training_data.append({"class":"票价", "sentence":"票价是多少钱"})

training_data.append({"class":"类型", "sentence":"类型是什么"})
training_data.append({"class":"类型", "sentence":"是什么类型的?"})
training_data.append({"class":"类型", "sentence":"是什么样的?"})
training_data.append({"class":"类型", "sentence":"是什么类型的景点?"})

words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = TraditionalChinese2SimplifiedChinese(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [w for w in words if w not in ignore_words]
words = list("".join(OrderedDict.fromkeys(words)))
# remove duplicates
classes = list(set(classes))
# print (len(documents), "documents")
# print (len(classes), "classes", classes)
# print (len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # print(doc)
    # stem each word
    pattern_words = [word for word in pattern_words]
    # print(pattern_words)
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    print(classes.index(doc[1]))
    output.append(output_row)

# sample training/output
i = 0
w = documents[i][0]
print ([word for word in w])
print (training[i])
print (output[i])
jpype.shutdownJVM()
