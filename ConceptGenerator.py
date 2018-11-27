# encoding=utf8
import sys
import CosineSim
import GetRelation
import graphGen

from threading import Thread
import threading

reload(sys)
sys.setdefaultencoding('utf8')

import spotlight
import nltk
from spotlight import SpotlightException

filePath = sys.argv[1]

dbEntities = dict() # stores index as key and values as tuple( DBpediaEntities , sentence)
threadslist=list()
entCount=0
cosineThreshold=0.3
tlock = threading.Lock()


def getDBpediaEntities(text):
    global entCount
    res = set()
    try:
        annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate',text)
        for a in annotations:
            res.add(a['surfaceForm'])
            
    except SpotlightException as e:
        pass
        #print 'No entities found in sentence {} : {}\n'.format(i,sentences[i])
    except Exception as e:
        print text
        print "Exception: ",e
    with tlock as t :
        if len(res) > 0:
            dbEntities[entCount] = (res, text)
            entCount += 1

        if entCount % 10 == 0:
            print "processed sentences: ", entCount


def parseData():

    with open(filePath) as fo:
        for line in nltk.sent_tokenize(fo.read()):
            line = line.strip()
            if len(line) == 0:
                continue
            t = Thread(target=getDBpediaEntities, args=(line,))
            threadslist.append(t)


#Parsing the data file creating dbpedia Entities dictionary
parseData()

for t in threadslist:
    t.start()
for t in threadslist:
    t.join()

print "Total sent for entit ", len(dbEntities.keys())

resRelations=list()

print "Hold on finding relations among entities...."

totalKeys=len(dbEntities.keys())

onePercent = float(totalKeys) / 100
counter=0


for d in dbEntities.keys():
    s = [x.lower() for x in set(dbEntities[d][0])]
    rels = GetRelation.getRelation(dbEntities[d][1])
    for rel in rels:
    	if rel[0].lower() in s and rel[2].lower() in s:
            if CosineSim.getCosineSim(rel[0],rel[2]) > cosineThreshold:
                resRelations.append(rel)
    #updating the per
    counter = counter + 1
    sys.stdout.flush()
    temp = "%d %% Completed" % (divmod(counter, onePercent)[0])
    sys.stdout.write('\r' + temp)
    sys.stdout.flush()

print "\nTotal Relations found ",len(resRelations)


print "Generating Graph..."

graphGen.GenerateGraphvizGraph(resRelations)
graphGen.GenerateGraph(resRelations)
