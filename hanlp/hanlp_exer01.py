import jpype
import pyhanlp
# tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')

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
def NLP_tokenizer(sentence_str):
    NLPTokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
    return NLPTokenizer.segment(sentence_str)
def Place_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enablePlaceRecognize(True)
    return HanLP.segment(sentence_str)
def PersonName_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enableNameRecognize(True)
    return HanLP.segment(sentence_str)
def Organization_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enableOrganizationRecognize(True)
    return HanLP.segment(sentence_str)
def Digit_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enableDigitRecognize(True)
    return HanLP.segment(sentence_str)
def total_result(function_result_input):
    x = str(function_result_input)
    y = x[1:len(x)-1]
    y = y.split(',')
    return y
def time_result(total_result):
    z = []
    for i in range(len(total_result)):
        if total_result[i][-2:] == '/t':
            z.append(total_result[i])
    return z
def digit_result(total_result):
    z = []
    for i in range(len(total_result)):
        if total_result[i][-2:] == '/m':
            z.append(total_result[i])
    return z
def single_result(Type_Recognition,total_result):
    if Type_Recognition == 'place':
        Type = '/ns'
    elif Type_Recognition == 'person':
        Type = '/nr'
    elif Type_Recognition == 'organization':
        Type = '/nt'
    else:
        print ('请输入正确的参数：（place，person或organization）')
    z = []
    for i in range(len(total_result)):
        if total_result[i][-3:] == Type:
            z.append(total_result[i])
    return z
def dict_result(sentence_str):
    sentence = TraditionalChinese2SimplifiedChinese(sentence_str)
    total_dict = {}
    a = total_result(Place_Recognize(sentence))
    b = single_result('place',a)
    # print(len(b[1].replace('/ns','').replace(' ','')))
    c = total_result(PersonName_Recognize(sentence))
    d = single_result('person',c)
    e = total_result(Organization_Recognize(sentence))
    f = single_result('organization',e)
    g = total_result(NLP_tokenizer(sentence))
    h = time_result(g)
    k = total_result(NLP_tokenizer(sentence))
    l = digit_result(g)
    print(l)
    total_list = [i for i in [b,d,f,h]]
    total_dict.update(place = total_list[0],person = total_list[1],organization = total_list[2],time = total_list[3])
    jpype.shutdownJVM()#关闭JVM虚拟机
    return total_dict
# test_sentence="2018年武胜县新学乡政府大楼门前锣鼓喧天,6月份蓝翔给宁夏固原市彭阳县红河镇捐赠了挖掘机,中国科学院计算技术研究所的宗成庆教授负责教授自然语言处理课程,而他的学生现在正在香港看肉蒲团"
# print (dict_result(test_sentence))
# test_sentence1="2个成年人和1个儿童"
# print(dict_result(test_sentence1))