from collections import OrderedDict
ignore_words = ['?', '呢', '吗']
words = [[],[],[]]
classes = [[],[],[]]

training_data = [[],[],[]]
training_data[0].append({"class":"地址", "sentence":"地址是哪里?"})
training_data[0].append({"class":"地址", "sentence":"在哪?"})
training_data[0].append({"class":"地址", "sentence":"地址在哪里"})
training_data[0].append({"class":"地址", "sentence":"在什么地方?"})

training_data[1].append({"class":"票价", "sentence":"票价是多少"})
training_data[1].append({"class":"票价", "sentence":"需要多少钱"})
training_data[1].append({"class":"票价", "sentence":"门票多少钱"})
training_data[1].append({"class":"票价", "sentence":"票价是多少钱"})

training_data[2].append({"class":"类型", "sentence":"类型是什么呢"})
training_data[2].append({"class":"类型", "sentence":"是什么类型的?"})
training_data[2].append({"class":"类型", "sentence":"是什么样的?"})
training_data[2].append({"class":"类型", "sentence":"是什么类型的景点?"})

def corpus_vector():
    global ignore_words,training_data,words,classes
    for i in range(0, len(training_data)):
        for pattern in training_data[i]:
            w = list(pattern['sentence'])
            words[i].extend(w)
            if pattern['class'] not in classes[i]:
                classes[i].append(pattern['class'])
        words[i] = [w for w in words[i] if w not in ignore_words]
        words[i] = list("".join(OrderedDict.fromkeys(words[i])))
        classes[i] = list(set(classes[i]))

def data_vector(sentence):
    global ignore_words
    training = []
    corpus_vector()
    for i in range(0, 3):
        bag = []
        pattern_words = [w for w in list(sentence) if w not in ignore_words]
        for w in words[i]:
            bag.append(1) if w in pattern_words else bag.append(0)
        training.append(bag)
    return training

def cosVector(y):
    x = []
    length = len(y)
    for i in range(0, length):
        x.append(1)
    result1 = 0
    result2 = 0
    result3 = 0
    for i in range(len(x)):
        result1 += x[i]*y[i] #sum(X*Y)
        result2 += x[i]**2     #sum(X*X)
        result3 += y[i]**2     #sum(Y*Y)
    if (result2*result3)**0.5 == 0:
        return 0
    else:
        cos = result1/((result2*result3)**0.5)
        return cos

def classification_by_cos(sentence):
    global classes
    cos = []
    max = 0
    index = 0
    for i in range(len(classes)):
        cos.append(cosVector(data_vector(sentence)[i]))
        if cos[i] > max:
            max = cos[i]
            index = i
    return classes[index]

print(classification_by_cos('大概是什么型的'))