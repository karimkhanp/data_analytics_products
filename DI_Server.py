import argparse
from http import server

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from graphpipe import convert

from math import log, exp
from operator import mul
from math import e
from collections import Counter
import os
import  json, csv
import pickle
import gzip
import struct
import numpy as np


pos = dict()
neg = dict()
features = set()
totals = [0, 0]
delchars = ''.join(c for c in map(chr, list(range(128))) if not c.isalnum())

CDATA_FILE = "countdata.pickle"

class MyDict(dict):

    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0
    
    def __init__(self):
        self.train()
       

    def negate_sequence(self,text):
        """
        Detects negations and transforms negated words into "not_" form.
        """
        negation = False
        delims = "?.,!:;"
        result = []
        words = text.split()
        prev = None
        pprev = None
        for word in words:
            # stripped = word.strip(delchars)
            stripped = word.strip(delims).lower()
            negated = "not_" + stripped if negation else stripped
            result.append(negated)
            if prev:
                bigram = prev + " " + negated
                result.append(bigram)
                if pprev:
                    trigram = pprev + " " + bigram
                    result.append(trigram)
                pprev = prev
            prev = negated
    
            if any(neg in word for neg in ["not", "n't", "no"]):
                negation = not negation
    
            if any(c in word for c in delims):
                negation = False
    
        return result
    
    
    def train(self):
        global pos, neg, totals
        retrain = False
        
        # Load traind data
        if not retrain and os.path.isfile(CDATA_FILE):
            pos, neg, totals = pickle.load(open(CDATA_FILE,'rb'),encoding='latin1')
            
           
            
            return
    
    def classify2(self, text):
        words = set(word for word in self.negate_sequence(text) if word in pos or word in neg)
        if (len(words) == 0): return True, 0
        # Probability that word occurs in pos documents
        pos_prob = sum(log((pos[word] + 1) / (2 * totals[0])) for word in words)
        neg_prob = sum(log((neg[word] + 1) / (2 * totals[1])) for word in words)
        return (pos_prob > neg_prob, abs(pos_prob - neg_prob))

    def percentage_confidence(self, conf):
        return 100.0 * e ** conf / (1 + e**conf)    

    def classify_demo(self, input_data):
        final_result = {}
    
        # print "Classification started"
        # data = json.loads(input_data)
        # text = data['text']
        text = input_data.tostring().decode()
        print(type(text))
       
      
        
        # try:
      
        words = set(word for word in self.negate_sequence(text) if word in pos or word in neg)
       
        
        # if (len(words) == 0): 
        #     print("No features to compare on")
        #     return 'True'
        flag, confidence = self.classify2(text)
       
        if confidence > 0.5:
            sentiment = "Positive" if flag else "Negative"
        else:
            sentiment = "Neutral"
        sentiment = [sentiment]

        return np.array(sentiment)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=10000, help="TCP port", type=int)
    args = parser.parse_args()
    server_address = ('', args.port)

    class sentimentscore():
        def __init__(self,data):
            self.data = data.tostring().decode()
           
        def sentiment(self):
            data = json.loads(self.data)
            sentance = ""
            if data.get('title'):
                print(data.get('title'),'title')
                sentance += data.get('title') + '.'
            if data.get('description'):
                sentance += data.get('description') + '.'
            if data.get('content'):
                sentance += data.get('content')
            outp = model.classify2(sentance)
            score = outp[1]
            flag = outp[0]

            sentimentval = None
            if score < 0.5:
                sentimentval = 3
            if score >0.5 and score <= 0.75 and  flag == True:
                sentimentval = 4
            if score >0.75 and   flag == True:
                sentimentval = 5
            if score >0.5 and score <=0.75 and  flag == False:
                sentimentval = 2
            if score >0.75 and flag == False:
                sentimentval = 1
            self.sentimentval = sentimentval
            data['sentiment'] = sentimentval
            return sentimentval

        def sentimentserver(self):
                
                return np.array([str(self.sentiment())])



    class GPHandler(server.BaseHTTPRequestHandler):

        def do_POST(self):
            inp = self.rfile.read(int(self.headers['Content-Length']))
            req = convert.deserialize_request(inp).input_tensors[0]
            reqcheck = str(req)
            if "Sentimentico@#$" in reqcheck:
                print ("\nSentimental_analsis")
                outp = sentimentscore(req).sentimentserver()
            else:
                print ("\nTwitter_analsis")
                outp = model.classify_demo(req)
            output_enc = convert.serialize_infer_response(outp)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(output_enc)
            

    httpd = server.HTTPServer(server_address, GPHandler)

    model = MyDict()

    print('Starting graphpipe sklearn server on port %d...' % args.port)
    while(True):
        httpd.handle_request()
