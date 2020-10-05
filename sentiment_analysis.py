from Base_py.base_file import *
from Base_py.NLP2novratio_sentnum import summarize


def stringformat(data):
    return re.sub(' +', ' ',data.replace('\r','').replace('\n',' '))

def Sentiment_Analysis():
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

    except KeyError:
        pass

    if len(content) == 0:
        flash('Please select any input channel and fill data')
        return redirect(url_for('textsummary'))

    x = summarize(content)
    wordres = x.showsentence()
    paragraph = ' '.join(wordres)
    paragraph = paragraph + "Sentimentico@#$"
    data = {}
    data['content'] = stringformat(paragraph)
    data['senticheck'] = stringformat("Sentiment_Analysis")
    data = json.dumps(data)
    print(data, 'data')
    print(type(data))
    query = np.array(data)
    print(query, 'query')
    print(type(query))
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
    args = parser.parse_args()
    y = query
    print ("y",y)
    pred = remote.execute(args.url, y)

    sentiment = pred.tobytes().decode()
    displaysentiment = int(sentiment)
    percent2 = 20 * int(sentiment)
    test1 = x.bestword1()
    ratiosum = x.sumratio()

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
    wordres = [val.replace('\n', ' ') for val in wordres]
    print ("test1 =",test1)
    return wordres, sntc, best, sen, test1, paragraph, sentiment, percent2, displaysentiment


class ParaSenti(Resource):
    def get(self):
        return {'about':'Enter your Paragraph'}
    def post(self):
        data = request.get_json()
        paragraph = data['paragraph']
        x = summarize(paragraph)
        wordres = x.showsentence()
        paragraph = ' '.join(wordres)
        paragraph = paragraph + "Sentimentico@#$"
        data = {}
        data['content'] = stringformat(paragraph)
        data['senticheck'] = stringformat("Sentiment_Analysis")
        data = json.dumps(data)
        print(data, 'data')
        print(type(data))
        query = np.array(data)
        print(query, 'query')
        print(type(query))
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
        args = parser.parse_args()
        y = query
        print("y", y)
        pred = remote.execute(args.url, y)

        sentiment = pred.tobytes().decode()
        displaysentiment = int(sentiment)



        summary = x.sumratio()
        best = x.bestword1()
        return {'Summary ':summary,'Keywords':best, "Sentimentscore" : displaysentiment}

class LinkSenti(Resource):
    def get(self):
        return {'about':'Enter your link'}
    def post(self):
        data = request.get_json()
        url = data['url']
        ratio = 40
        article = Article(url)
        article.download()
        article.parse()
        text=article.text
        x = summarize(text)
        wordres = x.showsentence()
        paragraph = ' '.join(wordres)
        paragraph = paragraph + "Sentimentico@#$"
        data = {}
        data['content'] = stringformat(paragraph)
        data['senticheck'] = stringformat("Sentiment_Analysis")
        data = json.dumps(data)
        print(data, 'data')
        print(type(data))
        query = np.array(data)
        print(query, 'query')
        print(type(query))
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
        args = parser.parse_args()
        y = query
        print("y", y)
        pred = remote.execute(args.url, y)

        sentiment = pred.tobytes().decode()
        displaysentiment = int(sentiment)
        summary = x.sumratio()
        best=x.bestword1()
        return {'Summary':summary,'Keywords':best, "Sentimentscore" : displaysentiment}
