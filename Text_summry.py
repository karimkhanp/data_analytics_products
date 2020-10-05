from Base_py.base_file import *
from Base_py.NLP2novratio import summarize
from Base_py.nounER import getEntities

textsummary = Blueprint('textsummary', __name__)


summryapi = Api(textsummary)
API_KEY = '1d63f3d5345c4fb9b645958435a27c74'  # f661fe8666e84aa0b52564da293e56d3
COUNTRY = 'gb'  # United kingdom
cloud = True

#for test server of text summarisation
global data_array
data_array = []


def Text_Summary_View():
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
            getratio = int(request.form['ratio1'])
            numlines = int(request.form['sentnum1'])
            sentlength = int(request.form['sentlength1'])
            wordlength = int(request.form['wordlength1'])
            try:
                best_chck = request.form.get('best_words1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                sen_chck = request.form.get('sen_score1')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                sntc_check = request.form.get('show_sentence1')
            except UnboundLocalError:
                pass
            try:
                ner_bullet = request.form.get('ner_bullet1')
            except UnboundLocalError:
                pass
    except UnboundLocalError:
        pass
    try:
        gettext = request.form.get('text')
        if gettext:
            testlist = len([val for val in gettext.split('.')])

            if testlist < 3:
                flash('Enter more then two sentences')
                return redirect(url_for('textsummary'))
            else:
                plain = gettext
                content = plain

            getratio = int(request.form['ratio2'])
            numlines = int(request.form['sentnum2'])
            sentlength = int(request.form['sentlength2'])
            wordlength = int(request.form['wordlength2'])
            try:
                best_chck = request.form.get('best_words2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                sen_chck = request.form.get('sen_score2')
            except UnboundLocalError:
                pass
            # ---------------------------
            try:
                sntc_check = request.form.get('show_sentence2')
            except UnboundLocalError:
                pass
            try:
                ner_bullet = request.form.get('ner_bullet2')
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
        getratio = int(request.form['ratio3'])
        numlines = int(request.form['sentnum3'])
        sentlength = int(request.form['sentlength3'])
        wordlength = int(request.form['wordlength3'])
        try:
            best_chck = request.form.get('best_words3')
        except UnboundLocalError:
            pass
        # ---------------------------
        try:
            sen_chck = request.form.get('sen_score3')
        except UnboundLocalError:
            pass
        # ---------------------------
        try:
            sntc_check = request.form.get('show_sentence3')
        except UnboundLocalError:
            pass
        try:
            ner_bullet = request.form.get('ner_bullet3')
        except UnboundLocalError:
            pass
    except KeyError:
        pass

    if len(content) == 0:
        flash('Please select any input channel and fill data')
        return redirect(url_for('textsummary'))

    fn_ratio = getratio / 100
    ratio = fn_ratio
    x = summarize(content, ratio)
    wordres = x.linesselect(numlines)
    content = wordres
    wordres = x.minsenlen1(sentlength)
    wordres = x.minwordlen1(wordlength)
    paragraph = ' '.join(wordres)
    test1 = x.bestword1()
    ratiosum = x.sumratio()
    # --------------
    if best_chck:
        best = x.bestword1()
    else:
        best = 0

    if sen_chck:
        sen = x.summarize_corpus()
    else:
        sen = 0

    if sntc_check:
        sntc = x.showsentence()
    else:
        sntc = 0

    if ner_bullet:
        nouns = x.get_nouns()
    else:
        nouns = 0
    wordres = [val.replace('\n', ' ') for val in wordres]
    return (wordres, sntc, best, sen, test1,
                           paragraph, nouns)


##################################################################################################
########################           API SECTION            ########################################

class Parsumr(Resource):
    def get(self):
        return {'about': 'Enter your Paragraph'}

    def post(self):
        timestamp = str(datetime.datetime.now())
        data = request.get_json()
        paragraph = data['paragraph']
        ratio = data['ratio']
        x = summarize(paragraph, ratio / 100)
        summary = x.sumratio()

        return {'Original_text': paragraph, 'Summary ': summary}, 201


class Linksumr(Resource):
    def get(self):
        return {'about': 'Enter your link'}

    def post(self):
        timestamp = str(datetime.datetime.now())
        data = request.get_json()

        url = data['url']
        ratio = data['ratio']
        article = Article(url)
        article.download()
        article.parse()

        # ners = getEntities("".join(article['text']))
        text = article.text
        ners = getEntities("".join(text))
        x = summarize(text, ratio / 100)
        summary = x.sumratio()
        best = x.bestword1()

        return {'Original_text': "".join(text), 'Summary': "".join(summary), 'Keywords': best, 'NERs': ners}


class EntitySumr(Resource):
    def get(self):
        return {"message": "No Paragraph for Entity Extraction"}

    def post(self):
        data = request.get_json()
        content = data["paragraph"]
        ent = getEntities(content)
        return {"entities": ent}


class returnSummary(Resource):
    def post(self):
        contents = []
        newsapi = NewsApiClient(api_key=API_KEY)
        headlines = newsapi.get_top_headlines(country=COUNTRY)
        articles = headlines['articles']
        try:
            import pdb
            # pdb.set_trace()
            for article in articles:
                element = {}
                # print(article.keys())
                element['original_text'] = article['content']
                element['source_URL'] = article['source']['name']
                element['author'] = article['author']
                element['title'] = article['title']
                element['url'] = article['url']
                element['source'] = article['source']['name']
                element['img_URL'] = article['urlToImage']
                element["news_posted_at"] = article["publishedAt"]
                abs_URL = article['url']
                if abs_URL:
                    article = Article(abs_URL)
                    article.download()
                    article.parse()
                    sm_obj = summarize(article.text, 0.2)
                    element['text'] = " ".join(sm_obj.linesselect(5))
                    print("Fetching from: ", abs_URL)

                element['NERs'] = getEntities("".join(element['text']))
                print(element)
                ##print(element['NERs'])
                contents.append(element)
                # print(contents)
                if len(contents) == 10:
                    break

        except:
            pass
        return {"summary": contents}


summryapi.add_resource(Parsumr, '/para')
summryapi.add_resource(Linksumr, '/link')
summryapi.add_resource(EntitySumr, "/enti")
summryapi.add_resource(returnSummary, "/summary")


