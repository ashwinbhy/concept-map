from pycorenlp import *

nlp = StanfordCoreNLP("http://localhost:9000/")


def getRelation(sen):
    res = list()
    output = nlp.annotate(sen, properties={"annotators": "tokenize,ssplit,pos,depparse,natlog,openie",
                                           "outputFormat": "json",
                                           "openie.triple.strict": "true",
                                           "openie.max_entailments_per_clause": "1"})
    result = [output["sentences"][0]["openie"] for item in output]
    for i in result:
        for rel in i:
            res.append((rel['subject'], rel['relation'], rel['object']))
    return res
