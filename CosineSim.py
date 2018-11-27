import pysolr
import nltk
import numpy as np

solr = pysolr.Solr('http://localhost:8983/solr/glove', timeout=10)


def getVectorFromSolr(word):
    result = solr.search("id:" + word)
    return result.raw_response['response']['docs'][0]['value'][0].split(" ")

def getVector(word):
    word=word.lower().strip()
    wList=nltk.word_tokenize(word)
    count=0
    res=np.zeros(100,dtype=float)
    for w in wList:
        temp=np.array(getVectorFromSolr(w),dtype=float)
        res=np.add(res,temp)
        count+=1
    res=np.divide(res,count)
    return res

def getCosineSimBetVectors(vec1,vec2):
    sim = max(0, np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return sim

def getCosineSim(word1,word2):
    vec1=getVector(word1)
    vec2=getVector(word2)
    return getCosineSimBetVectors(vec1,vec2)

