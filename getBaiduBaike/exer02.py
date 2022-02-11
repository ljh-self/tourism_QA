import re

def search_question(sentence):
    answer = []
    intention = re.match(r'(.*)(搜|查|知道)(.*?)', sentence)
    if intention:
        answer.append(True)
        questionId = re.findall(r'\d', sentence)[0]
        answer.append(questionId)
    else:
        answer.append(False)
    return answer
if __name__ == '__main__':
    answer1 = search_question('我要搜索3题')
    print(answer1[0])
    print(answer1[1])
    answer2 = search_question('我要查第3题')
    print(answer2[0])
    print(answer2[1])
    answer3 = search_question('搜第3题')
    print(answer3[0])
    print(answer3[1])