from keras.models import load_model
import re
from keras.preprocessing import sequence
import pickle
from numpy import argmax
from Base_py.base_file import *
from Base_py.NLP2novratio import summarize
from Base_py.nounER import getEntities

global get_input
model = load_model('hate_speech_model.h5')

with open('tokenizer.pickle', 'rb') as handle:
  token = pickle.load(handle)

label=['hate_speech', 'offensive_language', 'neither']

def clean_text(data):
  txt = data
  txt=re.sub(r'@[A-Z0-9a-z_:]+','',txt)
  txt=re.sub(r'^[RT]+','',txt)
  txt = re.sub('https?://[A-Za-z0-9./]+','',txt)
  txt=re.sub("[^a-zA-Z]", " ",txt)   
  return data

def padding(token, X):
  sequences=token.texts_to_sequences(X_train)
  pad_sequence=sequence.pad_sequences(sequences)
  return pad_sequence

   
def get_input(text): 
  text = text
  text=clean_text(text)
  seq=token.texts_to_sequences([text])
  pad = sequence.pad_sequences(seq)
  prediction = model.predict(pad)
  print(prediction)
  return (text, prediction[0], label, argmax(prediction[0]))


def Hate_speech_Func():
    #calling the functions ........
    content = ''
    try:
        geturl = request.form.get('url')
        print("IN get URL...  1")
        if geturl:
            print("IN get URL...  2") 
            url = geturl
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            content = text
    except UnboundLocalError:
        pass


    try:
        gettext = request.form.get('text')
        content = gettext
        if gettext:
            testlist = len([val for val in gettext.split('.')])
    except UnboundLocalError:
        pass



    try:
        file = request.files['file']
        # -----------------
        if file:
            pdf = request.files['file']
            # y = pdf.read().decode('utf-8')
            # pdf.save(secure_filename(pdf.filename))
            x = (pdf.filename).split(".")
            x = x[1]
            if x == 'pdf':
                pdf.save(secure_filename(pdf.filename))
                text = textract.process(pdf.filename).decode('utf-8')
                # print(type(text))
                print(text)
                content = text.replace('\n', ' ')
            else:
                y = pdf.read().decode('utf-8')
                content = y
    except KeyError:
        pass



    if len(content) == 0:
        flash('Please select any input channel and fill data')
      
    text, prediction, category, max= get_input(content)
    
    return (text, prediction, category, max ,content)
    


  
  
class hatespeechapi(Resource):
    def get(self):
        return {'about':'Enter your Paragraph'}
    def post(self):
        data = request.get_json()
        content = data['paragraph']
        text, prediction, category, max= get_input(content)
        return {'text':text,
                'prediction':prediction, 
                "category" : category,
                "max" : max
                }

