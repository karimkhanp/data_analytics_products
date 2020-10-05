from graphpipe import remote
import numpy as np
import argparse
from http import server

'''
This class will train and test the data and will give suspected class as result
'''
class SentimentAnalysis(object):
    """
    Init for client request
    """
    def __init__(self):
        pass
        
    def sendRequest(self):
        query = input("Enter Input Json")
        print(type(query))
        query = np.array(query)
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", default="http://127.0.0.1:10000",help="Url", type=str)
        args = parser.parse_args()
        y = query
        pred = remote.execute(args.url, y)
        sentiment = pred.tobytes().decode()
        print(sentiment)
    
if __name__ == '__main__':
    
    SentimentAnalysis().sendRequest()
    

