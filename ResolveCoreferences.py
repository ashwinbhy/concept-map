import xmltodict
import nltk
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


sentencesdict=dict()

doc=dict()

fileName='india'
pathTosf='/home/ashwin/Study/NLP/stanford-corenlp-full-2017-06-09/'

os.system('cp '+fileName +' '+pathTosf+fileName)

os.chdir(pathTosf)

print 'generating xml'

#os.system('java -Xmx3g -cp stanford-corenlp-3.8.0.jar:stanford-corenlp-models-3.8.0.jar:* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,mention,coref -coref.algorithm neural -file '+fileName)

print 'xml generated'

with open(fileName+'.xml') as fd:
    doc = xmltodict.parse(fd.read())

sentences=doc['root']['document']['sentences']['sentence']
print type (sentences)
for sen in sentences:
    #print "sentence no: ",sen['@id']
    tks=list()
    for token in sen['tokens']['token']:
        tks.append(token['word'])
    sentencesdict[sen['@id']]=' '.join(tks)
#for sen in sentencesdict.keys():
#    print sen,sentencesdict[sen]

coref=doc['root']['document']['coreference']['coreference']

for men in coref:
    for i in range(1,len(men['mention'])):
        senrepid=men['mention'][i]['sentence']
        if nltk.pos_tag([men['mention'][i]['text']],tagset='universal')[0][1]=='PRON':
            sentencesdict[senrepid]=sentencesdict[senrepid].replace(men['mention'][i]['text'],men['mention'][0]['text'])

print "After \n\n"
senno=sentencesdict.keys()
senno=sorted(senno)
newFile=open('clean'+fileName,"w")
for sen in senno:
        print sentencesdict[sen]
        newFile.write(sentencesdict[sen]+"\n")
newFile.close()