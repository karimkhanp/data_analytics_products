from flask import Flask, render_template, request
from Twitter_analytics import *
from Text_summry import *
from sentiment_analysis import *
from Base_py.base_file import *
from flask_restful import Resource, Api
from Base_py.NLP2novratio import summarize
from SpacyFunc import Spacy_NLP_Func, ParaNLP, LinkNLP
import datetime
from Hatespeech import *
import create_plot
import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import matplotlib.pyplot as plt 





app = Flask(__name__)
app.register_blueprint(twitterapp, url_prefix='/twitteranalytics')
app.register_blueprint(textsummary, url_prefix='/textsummary')

app.config['SECRET_KEY'] = 'b58f1ad3ab27a913c64246143682ebf5'
API_Reference = Api(app)

cwd = os.getcwd()
UPLOAD_FOLDER =cwd + '\\static\\Files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





@app.route('/googlec41563d4fdeb5c37', methods=['POST'])
def googlec41563d4fdeb5c37():
    return render_template("googlec41563d4fdeb5c37.html")


@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template("index.html")
    # print("hii")
    if request.method == 'POST':
        Name = request.form['name']
        Phone_Number = request.form['phone']
        Email = request.form['email']
        Message = request.form['message']
        new_data = {}
        new_data['name'] = Name
        new_data['phone'] = Phone_Number
        new_data['email'] = Email
        new_data['message'] = Message
        print(new_data)
    print("-----------------------------------------------------------------")
    return render_template("index.html")


@app.route('/twitterdata')
def my_form():
    print("Entered the twitter---------loop")
    Hashtag_dict, tren, ret_data, testlist, stringFrequencycount, sample_data = maindats()
    return render_template('maintwitterpage.html', Hashtag_dict=Hashtag_dict, tren=tren, ret_data=ret_data,
                           testlist=testlist,
                           javasample=stringFrequencycount, final_freq_Dict=sample_data)


@app.route('/twitterdata', methods=['POST'])
def my_form_post():
    Hashtag_dict, tren, ret_data, testlist, stringFrequencycount, sample_data = maindatspost()
    return render_template('maintwitterpage.html', Hashtag_dict=Hashtag_dict, tren=tren, ret_data=ret_data,
                           testlist=testlist,
                           javasample=stringFrequencycount, final_freq_Dict=sample_data)


@app.route('/twitterdata/trendsearch/<string:Key_Word>')
def my_form_trends(Key_Word):
    Hashtag_dict, tren, ret_data, testlist, stringFrequencycount, sample_data = my_form_trends_post(Key_Word)
    return render_template('maintwitterpage.html', Hashtag_dict=Hashtag_dict, tren=tren, ret_data=ret_data,
                           testlist=testlist,
                          javasample=stringFrequencycount, final_freq_Dict=sample_data)


@app.route('/textsummarypage', methods=['GET'])
def textsummary():
    contents = []
    return render_template('maintextsummariser.html', contents=contents)



@app.route('/textsummarypage_post' , methods=['POST'])
def textsummary_post():
    wordres , sntc, best, sen, test1, paragraph, nouns = Text_Summary_View()
    return render_template('post_maintextsummariser.html', wordres=wordres, sntc=sntc, best=best, sen=sen, test1=test1,
                        paragraph=paragraph, nouns=nouns)

@app.route('/sentimentpage', methods=['GET'])
def sentimentpage():
    contents = []
    return render_template('mainsentimentpage.html', contents=contents)



@app.route('/sentimentpage_post' , methods=['POST'])
def sentimentpage_post():
    wordres, sntc, best, sen, test1, paragraph, sentiment, percent2, displaysentiment = Sentiment_Analysis()
    print ("percent2 = ",percent2)
    return render_template('post_mainsentimentpage_final.html', wordres=wordres, sntc=sntc, best=best, sen=sen, test1=test1,
                           paragraph=paragraph, sentiment=sentiment, percent=percent2,
                           displaysentiment=displaysentiment,submit="submit")

@app.route('/Spacy' , methods=['GET'])
def spacy():
    return render_template('Spacy_get.html')


@app.route('/Spacy_post' , methods=['POST'])
def spacy_post():
    lngstc_anntatns_res,tokenzn_res,POSW_res,nmd_entits_res,vcblry_anntatns_res,content = Spacy_NLP_Func()
    return render_template('Spacy_post.html',lngstc_anntatns_res= lngstc_anntatns_res,tokenzn_res=tokenzn_res,
                                POSW_res=POSW_res,nmd_entits_res=nmd_entits_res,vcblry_anntatns_res=vcblry_anntatns_res,content = content)


@app.route('/HateSpeech' , methods=['GET'])
def HateSpeech():
    return render_template('HateSpeech.html')

@app.route('/HateSpeech_Post' , methods=['POST'])
def HateSpeech_Post():

    text, prediction, category, max ,content = Hate_speech_Func()
    return render_template('HateSpeech_Post.html',text=text, prediction=prediction, category=category, max=max,content = content)


@app.route("/dataset_info")
def dataset_info():
    path = os.getcwd()
    file = path + os.path.join('\\static\\images', 'category_analysis_hobbies.png')
    print(file)
    return render_template('dataset_info.html', user_image= file)



@app.route("/threshold_Create_Plot", methods=['POST', 'GET'])
def threshold_Create_Plot():
    # tvalue= -1 #default value
    #generating template data
    create_plot_check = "Disable"
    try:
        templateData = create_plot.template()
        if request.method == "POST":            
            category = str(request.form['category'])
            deptid = str(request.form['deptid'])
            item = str(request.form['item'])
            state = str(request.form['state'])
            storeid = str(request.form['storeid'])
            
            graphJSON = create_plot.plot(category, deptid, item, state, storeid)
            create_plot_check = "Enable"
            return render_template('threshold_Create_Plot.html', **templateData , plot=graphJSON,create_plot = create_plot_check)
    except:
        create_plot_check = "Error"
        print(create_plot_check)
    return render_template('threshold_Create_Plot.html', **templateData,create_plot = create_plot_check)



@app.route("/face_mask_detection", methods=['POST', 'GET'])
def face_mask_detection():

    
     
    def load_model():
        cwd = os.getcwd()
        with open('model.json', 'r') as json_file:
            loaded_model_json = json_file.read()

        loaded_model = model_from_json(loaded_model_json)
        loaded_model.summary()
        loaded_model.load_weights('weights.h5')
        print("Model loaded...")
        return loaded_model

    # detect face mask:
    def detect_face_mask(img):
        
        global loaded_model    
        label_dict = {0:'without_mask', 1:'mask'}
        color_dict = {0:(0, 0, 255), 1:(0, 255, 0)}
        
        dims = cascade.detectMultiScale(img)
        
        for (x,y,w,h) in dims:
            
            roi = img[y:y+h , x:x+w]
            #roi = cv2.cvtColor(roi, 1) #cv2.BGR2GRAY
            roi = cv2.resize(roi , dsize=(224, 224))
            normalized = roi/255.0
            reshaped=np.reshape(normalized,(1,224,224,3))
            reshaped = np.vstack([reshaped])
            result=loaded_model.predict(reshaped)
            #print(Class.shape)
                    
            label=np.argmax(result,axis=1)[0]
        
            cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
            cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
            cv2.putText(img, label_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
        return img
    
    
    
    if request.method == "POST": 
        import cv2
        cwd = os.getcwd()
        uploads_dir = cwd + '/static/Files'  
        try:
            file = request.files['file']
            # -----------------
            if file:
                mp4file = request.files['file']
                
                x = (mp4file.filename).split(".")
                x = x[1]
                if x == 'mp4':


                    uploaded_file = os.path.join(uploads_dir, secure_filename(mp4file.filename))
                    print(os.path.join(uploads_dir, secure_filename(mp4file.filename)))
                    mp4file.save(os.path.join(uploads_dir, secure_filename(mp4file.filename)))


                    mp4file.save(secure_filename(uploaded_file))
                    # Excution:
                    # Loading video:




                    video_path = uploaded_file # video
                    harr_path = "haarcascade_frontalface_default.xml"
                    cascade = cv2.CascadeClassifier(harr_path)

                    loaded_model = load_model()

                    # Real-time processing
                    cam = cv2.VideoCapture(video_path)
                    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

                    writer = cv2.VideoWriter('Result.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))

                    i=0
                    while i<2000:
                        _, frame = cam.read()
                        frame = detect_face_mask(cv2.flip(frame , 1, 1))
                        writer.write(frame)
                        i+=1

                    cam.release()
                    writer.release()
                    cv2.destroyAllWindows()
                    print("Everything Done....")
        except KeyError:
            pass

    return render_template('face_mask_detection.html')


@app.route('/post_API')
def post_API():
    return render_template('API_Reference_Page.html')



#################################################################################################
#######################           API SECTION            ######################################

#TWITTER
API_Reference.add_resource(HelloWorld, '/twitterdata/twitterAPI')

#TEXT_SUMMARY
API_Reference.add_resource(Parsumr, '/textsummarypage/para')
API_Reference.add_resource(Linksumr, '/textsummarypage/link')
API_Reference.add_resource(EntitySumr, "/textsummarypage/enti")
API_Reference.add_resource(returnSummary, "/textsummarypage/summary")

#SENTIMENT ANALYSIS
API_Reference.add_resource(ParaSenti,'/sentimentpage/para')
API_Reference.add_resource(LinkSenti,'/sentimentpage/link')

#SPACY ANALYSIS API
API_Reference.add_resource(ParaNLP,'/ParaNLP/para')
API_Reference.add_resource(LinkNLP,'/LinkNLP/link')

#HATESPEECH ANALYSIS API
API_Reference.add_resource(hatespeechapi,'/hatespeech/para')




if __name__ == '__main__':
    app.run(debug=True)
