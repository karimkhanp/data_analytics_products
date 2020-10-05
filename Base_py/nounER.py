import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
from collections import Counter

nlp = en_core_web_sm.load()

def retEnt(content):
    global nlp
    data = nlp(content)
    #print(len(data))
    dat = {}
    i = 0
    for sent in data.sents:
        l = []
        for x in nlp(str(sent)).ents:
            l.append([x.text,x.label_])
        dat[i] = l
        i+=1
    return dat           


def getEntities(content):
    res = retEnt(content)
    dates = []
    persons = []
    locations = []
    organizations = []
    entities = {}
    for item in res.keys(): 
        for rec in res[item]: 
            if rec[1]=='PERSON': 
                    persons.append(rec[0]) 
            elif rec[1]=='DATE':  
                    dates.append(rec[0]) 
            elif rec[1]=='ORG':  
                    organizations.append(rec[0])  
            elif rec[1]=='GPE' or rec[1]=='LOC':  
                    locations.append(rec[0])  
    entities["location"] = locations
    entities["person"] = persons
    entities["date"] = dates
    entities["organization"] = organizations
    return entities
