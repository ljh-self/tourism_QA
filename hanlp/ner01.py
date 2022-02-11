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

if __name__ == '__main__':
    test_sentence="首先我们为大家介绍的是中国丝绸5000年的发展过程。中国是最早发明家蚕养殖和丝织技艺的国家，自古就有丝国之称，至今仍然是世界丝绸产业的龙头。展品——陶纺轮 这是杭州良渚遗址出土的陶纺轮，大体呈圆饼形或凸圆形，中间有孔，插入木柄或骨柄可以捻线，是新石器时代文化遗址中较为常见的纺织生产工具。展柜里展放的是20世纪50年代在浙江省湖州市钱山漾遗址中发现的绢片复制品。我校教授徐辉、李茂松教授曾参与当年出土残片的考证。这是当时用于扫描的生物显微镜和复制蜡模，也是本厅的镇厅之宝。这里展示的是清代的土丝，土丝是指蚕农所采集的土种蚕茧所烧制成的低级的生丝"
    print (dict_result(test_sentence))