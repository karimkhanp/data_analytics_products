
# coding: utf-8

# In[71]:


import gensim 
import logging
print('gensim Version: %s' % (gensim.__version__))
from nltk import word_tokenize, pos_tag,sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
#from app import view
from gensim.summarization.pagerank_weighted import pagerank_weighted as _pagerank
from gensim.summarization.commons import build_graph as _build_graph
from flask import jsonify,make_response
import re

'''
word = int(input("Enter the Word Required"))
numlines = int(input("Select numbers of lines you want in output"))
minsenlen = int(input("Select minimum sentence length"))
minwordlen = int(input('Select Minimum word length'))
'''

logger = logging.getLogger(__name__)

class summarize:
    def __init__(self,content):#,word,numlines,minsenlen,minwordlen):
        self.content = content
        self.ratio = 1
        self.content_aftersent = ""
        self.content_forword = ""
    
    def sumratio(self):
        ''' Summarize based on the ration of original content required'''
        summarized = gensim.summarization.summarize(self.content,ratio=self.ratio)   
        tokenized_sent = sent_tokenize(summarized)
        return tokenized_sent

    
    def sumword(self,word):
        ''' Summarize based on the  word count '''
        summarized1 = gensim.summarization.summarize(self.content,word_count=word,ratio=self.ratio)
        tokenized_sent = sent_tokenize(summarized1)
        return tokenized_sent
    
    def linesselect(self,numlines):
        '''Selection Based on the lines required'''
        summarized2 = gensim.summarization.summarize(self.content,ratio=self.ratio)
        tokenized_sent = sent_tokenize(summarized2)
        tokenized_sent = tokenized_sent[:numlines]
        self.content_aftersent = " ".join(tokenized_sent)
        return tokenized_sent
    
    def minsenlen1(self,minsenlen):

        
        '''Selection Based on the mininum  Sentence length required'''
        #summarized2 = gensim.summarization.summarize(self.content,ratio=self.ratio)
        tokenized_sent = sent_tokenize(self.content_aftersent)
        newsummary = []
       
        for val in tokenized_sent:
            if len(val)>minsenlen:
                newsummary.append(val)
         
        self.content_forword = " ".join(newsummary)
        return newsummary
        
    def minwordlen1(self,minwordlen):
        '''Selection Based on the minimum Word Length Required '''
        #summarized3 = gensim.summarization.summarize(self.content,ratio=self.ratio)
        tokenized_sent = sent_tokenize(self.content_forword)
        listindex = []
        stopword_list = stopwords.words('english')
        for val in tokenized_sent:
            y = val.split(" ")
            remove_stopword = [x for x in y if x not in stopword_list]
            for val1 in remove_stopword:
                if len(val1)<minwordlen:
                    listindex.append(val)
                    break
        for val1 in listindex:
            tokenized_sent.remove(val1)
        return tokenized_sent

    def test(self):
      x1 = ['store', 'image caption', 'use', 'kaisa', 'resources', 'resource', 'new', 'clothes', 'clothing', 'cloth', 'goods', 'good', 'giant', 'hand', 'tables', 'table', 'environment', 'peppi', 'kierratyskeskus', 'personal', 'hold', 'mission', 'neat', 'receipt', 'street', 'wardrobe', 'tuire', 'christmas', 'centre', 'centres', 'anytime', 'soon', 'recent', 'recently', 'said', 'hannamarie', 'cat', 'items', 'item', 'things', 'internet', 'dyes']
      return x1
		
    def bestword1(self):
       # summarize4 = gensim.summarization.summarize(self.content,ratio=self.ratio)
       bestword = gensim.summarization.keywords(self.content, ratio=0.9, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=False, deacc=True)
       bestword=bestword.split('\n')
       # print(type(bestword))
       # print(make_response(jsonify(bestword)))
       return bestword
    
    def showsentence(self):
        '''Display actual text sentence '''
        tokenized_sent = sent_tokenize(self.content)
		
        return tokenized_sent
#---------------------------------------------------
    def summarize_corpus(self):
      # print(self.content,'content')
      keywords = self.bestword1()
      summarized5 = self.sumratio()
      scorelist = []
      withoutscorelist = []
      scoretotal = []
      for val in summarized5:
          count = 0
          sentence = re.sub('[\(\)\{\}<>]', '', val)
    
          sentence = sentence.lower().split(' ')
          # sentence = val.lower().split(' ')
          for val1 in sentence:
              if val1 in keywords:
                  count += 1
          score = count/len(keywords)
          scoretotal.append(score)
          if score > 0:
              scorelist.append((val,score))
              withoutscorelist.append(val)
      if scoretotal[-1] == 0:
          minv = scoretotal[-2]
      else:
          minv = scoretotal[-1]

      # for val in scorelist:
      #     print(val[0])
      # for val in ratio:
      #     print(val)

      noscorelist = list(set(summarized5) - set(withoutscorelist))
      for val in noscorelist:
          scorelist.append((val,minv/(2**len(noscorelist))))
      finalscore = [(val,value) for val in summarized5 for key,value in scorelist if val in key]
      finalscore.sort(key = lambda x: x[1],reverse=True)
      # for val in summarized5:
      #     for key , value in scorelist:
      #         if val in key:
      #             finalscore.append((val,value))
                  


      return finalscore





       # summarized5 = gensim.summarization.summarize(self.content,ratio=self.ratio)
       # print(type(summarized5),'summarized5')
       # if len(summarized5) == 0:
       #  # logger.warning("Input text is empty.")
       #  # return []
       #  summarized5 = self.content
       # # tokenized_sent = sent_tokenize(summarized5)

       # tokenized_sent = sent_tokenize(self.content)
       # print(type(tokenized_sent),'tokenized_sent')
       # sen_list = []
       # for val in tokenized_sent:
       #     sen_list.append([val])
       # hashable_corpus = [tuple(doc) for doc in sen_list]
       # graph = _build_graph(hashable_corpus)
       # pagerank_scores = _pagerank(graph)
       # pageranklist = []
       # temp = [1,]
       # scoresum = 0
       # for key, value in pagerank_scores.items():
       #     temp = [[key[0]],[value]]
           
       #     scoresum += float(value)
       #     pageranklist.append(temp)


       #  # -----------sentence score/sum(score)-----------------------------
       # scorepagelist = []
       # tokensummarize = sent_tokenize(summarized5)
       # for val in tokensummarize:
       #  for val1 in pageranklist:
       #    if val in val1[0]:
       #      scorepagelist.append([val,((float(val1[1][0]))/scoresum)])
            
       #      print(type(float(val1[1][0])))
       #      print(type(val1[1]))
       #      print(type(scoresum),'scoresum')
       #      print((float(val1[1][0]))/scoresum)
       # print(scorepagelist) 
       # return scorepagelist
       #  # ----------------------------------------
       

       # # return pageranklist
    

        

