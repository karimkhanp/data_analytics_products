import spacy
from Base_py.base_file import *


global nlp,nlp_md,content

nlp = spacy.load("en_core_web_sm")
nlp_md = spacy.load("en_core_web_md")
# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
lngstc_anntatns_res_array = []
tokenzn_res_array= []
POSW_res_array= []
nmd_entits_res_array= []
vcblry_anntatns_res_array= []

def Linguistic_annotations(doc):
    doc = nlp(doc)
    print ("\nLinguistic_annotations ")
    for token in doc:
        lngstc_anntatns_res_array.append(str(token.text) + " -> "+ str(token.pos_) + " , "+ str(token.dep_))
    return lngstc_anntatns_res_array

def Tokenization(doc):
    doc = nlp(doc)
    print ("\nTokenization ")
    for token in doc:
        tokenzn_res_array.append(str(token.text))
    return tokenzn_res_array

def Part_of_speech_tags(doc):
    doc = nlp(doc)
    print ("\nPart_of_speech_tags")
    for token in doc:
        POSW_res_array.append(str(token.text) + " -> "+ str(token.lemma_ )+ " , "+ str(token.pos_) + " , "+ str(token.tag_ )+ " , "+ str(token.dep_ )+ " , "+
                str(token.shape_) + " , "+ str(token.is_alpha) + " , "+ str(token.is_stop))
    return POSW_res_array

def Named_Entities(doc):
    doc = nlp(doc)
    print ("\nNamed_Entities")
    for ent in doc.ents:
        nmd_entits_res_array.append(str(ent.text) + " -> "+ str(ent.start_char) + " , "+ str( ent.end_char) + " , "+ str(ent.label_))
    return nmd_entits_res_array

def Out_of_vocabulary(doc):
    print ("\nOut-of-vocabulary")
    tokens = nlp_md(doc)
    for token in tokens:
        vcblry_anntatns_res_array.append(str(token.text) + " -> "+ str(token.has_vector) + " , "+ str(token.vector_norm) + " , "+ str(token.is_oov))
    return vcblry_anntatns_res_array
    
def Spacy_NLP_Func():
    #calling the functions ........
    content = ''
    try:
        geturl = request.form.get('url')
        if geturl:
            url = geturl
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            content = text
            try:
                lngstc_anntatns = request.form.get('Linguistic_Annotations1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                tokenzn = request.form.get('Tokenization1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                POSW = request.form.get('Parts_of_Speech_Words1')
            except UnboundLocalError:
                pass
            try:
                nmd_entits = request.form.get('Named_Entities1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                vcblry_anntatns = request.form.get('Vocabulary_Annotations1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                NLP = request.form.get('NLP1')
            except UnboundLocalError:
                pass
            # ---------------------------
    except UnboundLocalError:
        pass
    try:
        gettext = request.form.get('text')
        content = gettext
        if gettext:
            testlist = len([val for val in gettext.split('.')])

            try:
                lngstc_anntatns = request.form.get('Linguistic_Annotations2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                tokenzn = request.form.get('Tokenization2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                POSW = request.form.get('Parts_of_Speech_Words2')
            except UnboundLocalError:
                pass
            try:
                nmd_entits = request.form.get('Named_Entities2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                vcblry_anntatns = request.form.get('Vocabulary_Annotations2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                NLP = request.form.get('NLP2')
            except UnboundLocalError:
                pass
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
            try:
                lngstc_anntatns = request.form.get('Linguistic_Annotations3')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                tokenzn = request.form.get('Tokenization3')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                POSW = request.form.get('Parts_of_Speech_Words3')
            except UnboundLocalError:
                pass
            try:
                nmd_entits = request.form.get('Named_Entities3')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                vcblry_anntatns = request.form.get('Vocabulary_Annotations3')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                NLP = request.form.get('NLP3')
            except UnboundLocalError:
                pass
    except KeyError:
        pass

    if len(content) == 0:
        flash('Please select any input channel and fill data')
        return redirect(url_for('textsummary'))

    if lngstc_anntatns:
        lngstc_anntatns_res = Linguistic_annotations(content)
    else:
        best = 0

    if tokenzn:
        tokenzn_res = Tokenization(content)
    else:
        best = 0
        
    if POSW:
        POSW_res = Part_of_speech_tags(content)
    else:
        best = 0
    
    if nmd_entits:
        nmd_entits_res = Named_Entities(content)
    else:
        best = 0

    if vcblry_anntatns:
        vcblry_anntatns_res = Out_of_vocabulary(content)
    else:
        best = 0

    if NLP:
        NLP_res = 0
    else:
        best = 0

    
    return lngstc_anntatns_res,tokenzn_res,POSW_res,nmd_entits_res,vcblry_anntatns_res,content
  
  
  
class ParaNLP(Resource):
    def get(self):
        return {'about':'Enter your Paragraph'}
    def post(self):
        data = request.get_json()
        content = data['paragraph']
        lngstc_anntatns_res = Linguistic_annotations(content)
        tokenzn_res = Tokenization(content)
        POSW_res = Part_of_speech_tags(content)
        nmd_entits_res = Named_Entities(content)
        vcblry_anntatns_res = Out_of_vocabulary(content)
        
        return {'content':content,
                'Linguistic_annotations':lngstc_anntatns_res, 
                "Tokenization" : tokenzn_res,
                "Part_of_speech_tags" : POSW_res,
                "Named_Entities" : nmd_entits_res,
                "Out_of_vocabulary" : vcblry_anntatns_res
                }



class LinkNLP(Resource):
    def get(self):
        return {'about':'Enter your link'}
    def post(self):
        data = request.get_json()
        url = data['url']
        article = Article(url)
        article.download()
        article.parse()
        content=article.text
        lngstc_anntatns_res = Linguistic_annotations(content)
        tokenzn_res = Tokenization(content)
        POSW_res = Part_of_speech_tags(content)
        nmd_entits_res = Named_Entities(content)
        vcblry_anntatns_res = Out_of_vocabulary(content)
        return {'content':content,
                'Linguistic_annotations':lngstc_anntatns_res, 
                "Tokenization" : tokenzn_res,
                "Part_of_speech_tags" : POSW_res,
                "Named_Entities" : nmd_entits_res,
                "Out_of_vocabulary" : vcblry_anntatns_res
                }


