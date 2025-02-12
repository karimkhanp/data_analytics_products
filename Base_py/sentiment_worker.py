
from math import log, exp
from operator import mul
from math import e
from collections import Counter
import os
import  json, csv
import pickle

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
        # print "Trained...."

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
        data = json.loads(input_data)
        text = data["text"]
        try:
            words = set(word for word in self.negate_sequence(text) if word in pos or word in neg)
            # if (len(words) == 0): 
            #     print("No features to compare on")
            #     return 'True'
            flag, confidence = self.classify2(text)
            if confidence > 0.5:
                sentiment = "Positive" if flag else "Negative"
            else:
                sentiment = "Neutral"
            conf = "%.4f" % self.percentage_confidence(confidence)
            final_result['sentiment'] = sentiment
            final_result['confidence'] = conf
            
            return json.dumps(final_result)
        except:
            import traceback
            # print traceback.format_exc()
            print("There is some error, please retry with different input")
            
# if __name__ == '__main__':
#    print('hi')
