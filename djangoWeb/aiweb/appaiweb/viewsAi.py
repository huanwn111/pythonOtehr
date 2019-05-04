import jieba.analyse
from gensim import corpora, models, similarities
import gensim
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#POST提交要加csrf，清除提交限制，底下加相关方法加@csrf_exempt
import json
from django.conf.urls.static import static
import os

'''
str = 'NCAA最强控卫是坎巴还是弗神新浪体育讯如今，本赛季的NCAA进入到了末段，各项奖项的评选结果也即将出炉。'
submitStr = ' '.join(jieba.analyse.extract_tags(str,topK=5,withWeight=False))
print(submitStr)
'''

#摘要关键词数
topK=50

#jiea TF-IDF 提取主题
#jieba.analyse.extract_tags用的是TF-IDF思想
#或用单纯的allwords.groupby().agg({"count":numpy.size})
#agg计数，再reset_index().sort_values(by=['count'])
#TF-IDF更有优势，考虑了高频词在整个语料库中出现次数的影响（与在语料库中出现的频率成反比，与自己频正比）
@csrf_exempt
def getSummary(request):
    rawText = request.POST.get('rawText')
    summary = ' '.join(jieba.analyse.extract_tags(rawText,topK=topK, withWeight=False))
    datas = {'summary':summary,'status':'success'}
    return HttpResponse(json.dumps(datas),content_type="application/json,charset=utf-8")
    #注意HttpResponse不能直接返回汉字字符串，拼到json串里用json.dumps可以

#LDA 生成词云
@csrf_exempt
def getCloud(request):
    rawText = request.POST.get('rawText')
    #jieba分词
    wordsList = jieba.lcut(rawText)
    #去停用词
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #filePath = os.path.join(BASE_DIR,"appaiweb\\static\\stopwords.text")
    stopWordsList = []
    with open(r'G:\vscWorkspace\djangoWeb\aiweb\appaiweb\static\stopwords.txt','r', encoding='utf-8') as fStop:
        stopWords = fStop.readlines()
        for sw in stopWords:
            stopWordsList.append(sw.split('\n')[0])
    #print("stopWords666666666",stopWords)
    wordsClean = []
    for wRaw in wordsList:
        if len(wRaw)>0 and wRaw not in stopWordsList:
            wordsClean.append(wRaw)
    coporaDocs = []
    coporaDocs.append(wordsClean)
    #print("coporaDocs1111111111",coporaDocs)
    #做映射，相当于词袋（词频与词对应格式）
    dict = corpora.Dictionary(coporaDocs)
    #print("dict111111111111",dict)
    corpus = [dict.doc2bow(s) for s in coporaDocs]
    lda = gensim.models.ldamodel.LdaModel(corpus = corpus, id2word=dict,num_topics=topK)
    #num_topics 最大主题数，类似k-means自己指定k
    print(lda.print_topic(1,topn=topK))
    for topic in lda.print_topics(num_topics=topK,num_words=topK):
        print(topic[1])
        summary = topic[1]
    #相似度比较
    #similarity = similarities.Similarity('发改委', corpus, num_features=400)
    #print("相似度111111111111",similarity)
    datas = {'summary':summary,'status':'success'}
    return HttpResponse(json.dumps(datas),content_type="application/json,charset=utf-8")
    #注意HttpResponse不能直接返回汉字字符串，拼到json串里用json.dumps可以
