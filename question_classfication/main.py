from question_classfication.data_process_exer01 import Question

if __name__ == '__main__':
    sentence = "类型为寺庙的景点有哪些"
    answer = Question().question_process(sentence)
    print(answer)