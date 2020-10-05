from Base_py.base_file import *

twitterapp = Blueprint('twitterapp', __name__)
twitter_api = Api(twitterapp)

# new secret key for Twitter Access
ckey = 'Js9Oa0JRZMhSfWxv22Pveg'
csecret = 'KSgDHAO6ohbyI5tvjQt0UOkc7pS0J3EjpAxBdjo3A'
atoken = '200582436-VjztFLtHsHRa8BuJEMuUvRph3xFu1zK6inptnWua'
asecret = 'Chib4KBPb1APNhLepSPp6loHpwVLwEai8bZ52l0o4JXj3'

# set the Twitter API Reference
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twapi = tweepy.API(auth, retry_count=10, retry_delay=5, retry_errors=set([131]))


# twitterapp.config['MAIL_SERVER'] = 'smtp.gmail.com'
# twitterapp.config['MAIL_PORT'] = 465
# twitterapp.config['MAIL_USERNAME'] = 'sherkhan.72.313@gmail.com'
# twitterapp.config['MAIL_PASSWORD'] = 'sherkhan_786'
# twitterapp.config['MAIL_USE_TLS'] = False
# twitterapp.config['MAIL_USE_SSL'] = True
# twitterapp.config['MAIL_DEFAULT_SENDER'] = 'sherkhan.72.313@gmail.com'
# mail = Mail(twitterapp)

def getTweets(Trend_Key_Word):
    global q
    global e
    global z1, z2, z3
    global flag
    global tren

    tren = []
    e = "Show All"
    z1 = ""
    z2 = ""
    z3 = ""

    if Trend_Key_Word == "home":
        try:
            if ("keyword1" in request.form):
                form_StrValue = request.form['keyword1']
            else:
                form_StrValue = request.form['keyword']
            form_StrValue = form_StrValue.split('$')

            print("Keyword =", form_StrValue[0])
            q = form_StrValue[0]
            e = form_StrValue[1]
        except:
            q = "twitter"
    else:
        try:
            q = Trend_Key_Word
        except:
            q = "twitter"
    try:
        e = e
    except:
        o = 0
    ####reverse_geocoding
    try:
        a = [i for i in q.split(',')]
        b = rg.search((float(a[0]), float(a[1])), mode=1)
        q = list(b[0].values())[2]
    except:
        o = 0
    coo = 0
    try:
        response = requests.get("http://ip-api.com/json/{}".format(request.remote_addr))
        js = response.json()
        print(js)
        qq = js['countryCode']
    except:
        g = geocoder.ip('me')
        print(g.ip)
        aa = [str(g.latlng[0]), str(g.latlng[1])]
        bb = rg.search((float(aa[0]), float(aa[1])), mode=1)
        print("bb")
        print(bb)
        qq = bb[0]['cc']
        print(qq)
    try:
        countr = pytz.country_names[str(qq)]
        client = yweather.Client()
        w = client.fetch_woeid(str(countr))

        print("w = ",w)
        trends1 = twapi.trends_place(w)
        data = trends1[0]
        trends = data['trends']
        for trend in trends[:10]:
            temp = trend['name']
            tren.append(temp)
    except:
        o = 0

    try:
        if ('keywordx' in request.form):
            q = request.form['keywordx']
            keyword = tweepy.Cursor(twapi.search, q, tweet_mode='extended', lang='en').items(50)
            coo = 1
    except:
        o = 0
    if (coo == 0):
        keyword = tweepy.Cursor(twapi.search, q, tweet_mode='extended', lang='en').items(50)

    return (keyword, tren)


def maindats():
    print("Entered the loop of the twitter")
    global y
    global flag, Hashtag_dict
    flag = 1
    q = "Twitter"
    keyword, tren = getTweets("home")
    ret_data = []
    analyzer = SentimentIntensityAnalyzer()
    positivecount = 0
    neutralcount = 0
    negativecount = 0
    alltweet = []
    filteredtweet = []

    # Getting the Latest Trends of INDIA..
    World_woeIDs_dict = {}
    Hashtag_dict = {}
    World_woeIDs = twapi.trends_available()
    World_woeIDs = json.loads(json.dumps(World_woeIDs, indent=1))
    for data in (World_woeIDs):
        World_woeIDs_dict[data["country"]] = data["woeid"]
    India_id = (World_woeIDs_dict['India'])
    for i in range(0, 10):
        try:
            world_trends = (twapi.trends_place(India_id))
            break
        except:
            print("attempt - ", i)
            pass
    world_trends = json.loads(json.dumps(world_trends, indent=1))
    for trend in world_trends:
        trend_array = (trend["trends"])
        for hashtag in trend_array:
            Hashtag_dict[(hashtag["name"].strip("#"))] = str((hashtag["tweet_volume"]))
            pass

    for tweet in keyword:
        p = "url"
        imageurl = ""
        co = 1
        ####articles
        if (e == "Article"):
            try:
                p = tweet._json["entities"]["urls"][0]["url"]
            except:
                o = 0
            if (p == "url"):
                continue
        ####
        ####Images
        if (e == "Image"):
            print('IMAGE')
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            y = ""
            try:
                y = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (y != "photo"):
                    co = 0
            except:
                o = 0
        ####
        ####Videos
        if (e == "Video"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            g = ""
            try:
                g = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (g != "video"):
                    co = 0
            except:
                o = 0
        ####
        ####GIF
        if (e == "GIF"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            w = ""
            try:
                w = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (w != "animated_gif"):
                    co = 0
            except:
                o = 0
        ####
        if (co == 1):
            PartialWord = ("@", "#", "https", "RT")
            word = tweet.full_text
            wordsplit = word.split(' ')
            wordjoin = [word for word in wordsplit if not word.startswith(PartialWord)]
            word = ' '.join(wordjoin)
            filteredtweet.append(word)
            vs = analyzer.polarity_scores(str(word))
            emoj = [values for key, values in vs.items()]
            emoj = emoj[:-1]
            query = word
            query = np.array(query)
            parser = argparse.ArgumentParser()
            parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
            args = parser.parse_args()
            y = query
            pred = remote.execute(args.url, y)

            y1 = pred.tobytes().decode()

            y = emoj.index(max(emoj))
            mannum = max(emoj)
            # print(vs)
            for tex, num1 in vs.items():
                if num1 == mannum:
                    num1 = round(num1 * 100, 2)
                    valueof = [tex, str(num1)]
                    strvalue = "-".join(valueof)
            if y1 == 'Negative':
                name = 'unamused face'
                negativecount += 1
            elif y1 == 'Neutral':
                name = 'neutral face'
                neutralcount += 1
            elif y1 == 'Positive':
                name = 'grinning face'
                positivecount += 1
            for emoji, name1 in analyzer.make_emoji_dict().items():
                if name1 == name:
                    emoji1 = emoji
            alltweet.append(tweet.full_text)

            '''data = [{'Created at':tweet.created_at},{'Tweet':tweet.full_text.encode('utf-8')},{'Retweet_count':tweet.retweet_count},{'Favourites_count':tweet.user.favourites_count},{'User_name':tweet.user.name.encode('utf-8')},{'Profile_img':tweet.user.profile_image_url},{'Followers_count':tweet.user.followers_count},{'Friends_count':tweet.user.friends_count}]'''
            '''data = [tweet.created_at, tweet.full_text.encode('utf-8'),vs,emoji1,tweet.retweet_count, tweet.user.favourites_count, tweet.user.name.encode('utf-8'), tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count]'''
            # if(e=="Image" or e=="Video" or e=="GIF"):
            data = [tweet.created_at, tweet.full_text, y1, emoji1, tweet.retweet_count, tweet.user.favourites_count,
                    tweet.user.name, tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count,
                    imageurl]
            ret_data.append(data)
    ####

    ret_data.sort(key=lambda x: x[5])
    ret_data.reverse()

    stringTweet = ','.join(alltweet)

    stopwordsadd = stopwords.words('english')
    stopwordsadd.extend(('RT', '@', ':', '...', '..', '...', '.As', 'dont', 'follow', ',', '#', 'https', '’', 'I', 's',
                         '?', '!', '(', '.', '&', 'amp', ';', "'s", "'", 'It', "n't", '“', '”', '``', "''", '-', ')',
                         '/', 'https…'))

    setstopwords = set(stopwordsadd)
    word_tokens = word_tokenize(stringTweet)

    filtered_sentence = [w for w in word_tokens if not w in setstopwords]

    filtered_sentence = []

    for w in word_tokens:
        if w not in setstopwords:
            filtered_sentence.append(w)

    fdist = FreqDist(filtered_sentence)

    frequencycount = []
    final_freq_Dict = []
    sample_data_comp = []
    stringFrequencycount = ''
    sample_data = ""
    counter = 0
    for word, frequency in fdist.most_common():
        if len(word) < 10:
            if frequency > 0:
                frequencycount.append(word)
                stringFrequencycount = ','.join(frequencycount)
                if counter < 200:
                    for i in range(0, frequency):
                        sample_data = sample_data + word + ","
                        # final_freq_Dict =sample_data
                    counter = counter + 1

    testlist = [{
        "label": "Positive",
        "value": positivecount
    }, {
        "label": "Neutral",
        "value": neutralcount
    }, {
        "label": "Negative",
        "value": negativecount
    }]

    return (Hashtag_dict, tren, ret_data,
            testlist,
            stringFrequencycount, sample_data)


def maindatspost():
    global y
    global flag
    flag = 0
    # q = "Twitter"
    keyword, tren = getTweets("home")
    ret_data = []
    analyzer = SentimentIntensityAnalyzer()
    positivecount = 0
    neutralcount = 0
    negativecount = 0
    alltweet = []
    filteredtweet = []

    for tweet in keyword:
        p = "url"
        imageurl = ""
        co = 1
        ####articles
        if (e == "Article"):
            try:
                p = tweet._json["entities"]["urls"][0]["url"]
            except:
                o = 0
            if (p == "url"):
                continue
        ####
        ####Images
        if (e == "Image"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            y = ""
            try:
                y = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (y != "photo"):
                    co = 0
            except:
                o = 0
        ####
        ####Videos
        if (e == "Video"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            g = ""
            try:
                g = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (g != "video"):
                    co = 0
            except:
                o = 0
        ####
        ####GIF
        if (e == "GIF"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            w = ""
            try:
                w = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (w != "animated_gif"):
                    co = 0
            except:
                o = 0
        ####
        if (co == 1):
            PartialWord = ("@", "#", "https", "RT")
            word = tweet.full_text
            wordsplit = word.split(' ')
            wordjoin = [word for word in wordsplit if not word.startswith(PartialWord)]
            word = ' '.join(wordjoin)
            filteredtweet.append(word)
            vs = analyzer.polarity_scores(str(word))
            emoj = [values for key, values in vs.items()]
            emoj = emoj[:-1]
            query = word
            query = np.array(query)
            parser = argparse.ArgumentParser()
            parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
            args = parser.parse_args()

            y = query

            pred = remote.execute(args.url, y)

            y1 = pred.tobytes().decode()

            y = emoj.index(max(emoj))
            mannum = max(emoj)
            # print(vs)
            for tex, num1 in vs.items():
                if num1 == mannum:
                    num1 = round(num1 * 100, 2)
                    valueof = [tex, str(num1)]
                    strvalue = "-".join(valueof)
            if y1 == 'Negative':
                name = 'unamused face'
                negativecount += 1
            elif y1 == 'Neutral':
                name = 'neutral face'
                neutralcount += 1
            elif y1 == 'Positive':
                name = 'grinning face'
                positivecount += 1
            for emoji, name1 in analyzer.make_emoji_dict().items():
                if name1 == name:
                    emoji1 = emoji
            alltweet.append(tweet.full_text)

            '''data = [{'Created at':tweet.created_at},{'Tweet':tweet.full_text.encode('utf-8')},{'Retweet_count':tweet.retweet_count},{'Favourites_count':tweet.user.favourites_count},{'User_name':tweet.user.name.encode('utf-8')},{'Profile_img':tweet.user.profile_image_url},{'Followers_count':tweet.user.followers_count},{'Friends_count':tweet.user.friends_count}]'''
            '''data = [tweet.created_at, tweet.full_text.encode('utf-8'),vs,emoji1,tweet.retweet_count, tweet.user.favourites_count, tweet.user.name.encode('utf-8'), tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count]'''
            # if(e=="Image" or e=="Video" or e=="GIF"):
            data = [tweet.created_at, tweet.full_text, y1, emoji1, tweet.retweet_count, tweet.user.favourites_count,
                    tweet.user.name, tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count,
                    imageurl]
            ret_data.append(data)
    ####

    ret_data.sort(key=lambda x: x[5])
    ret_data.reverse()

    stringTweet = ','.join(alltweet)

    stopwordsadd = stopwords.words('english')
    stopwordsadd.extend(('RT', '@', ':', '...', '..', '...', '.As', 'dont', 'follow', ',', '#', 'https', '’', 'I', 's',
                         '?', '!', '(', '.', '&', 'amp', ';', "'s", "'", 'It', "n't", '“', '”', '``', "''", '-', ')',
                         '/', 'https…'))

    setstopwords = set(stopwordsadd)
    word_tokens = word_tokenize(stringTweet)

    filtered_sentence = [w for w in word_tokens if not w in setstopwords]

    filtered_sentence = []

    for w in word_tokens:
        if w not in setstopwords:
            filtered_sentence.append(w)

    fdist = FreqDist(filtered_sentence)

    frequencycount = []
    sample_data = ''
    stringFrequencycount = ''
    counter = 0
    final_freq_Dict = []
    for word, frequency in fdist.most_common():
        if len(word) < 10:
            if frequency > 0:
                frequencycount.append(word)
                stringFrequencycount = ','.join(frequencycount)
                if counter < 200:
                    for i in range(0, frequency):
                        sample_data = sample_data + word + ","
                        # final_freq_Dict =sample_data
                    counter = counter + 1

    testlist = [{
        "label": "Positive",
        "value": positivecount
    }, {
        "label": "Neutral",
        "value": neutralcount
    }, {
        "label": "Negative",
        "value": negativecount
    }]
    return (Hashtag_dict, tren, ret_data, testlist, stringFrequencycount, sample_data)


def my_form_trends_post(Key_Word):
    global y
    global flag
    global Trend_Key_Word
    flag = 0
    Trend_Key_Word = Key_Word
    # q = "Twitter"
    keyword, tren = getTweets(Trend_Key_Word)
    ret_data = []
    analyzer = SentimentIntensityAnalyzer()
    positivecount = 0
    neutralcount = 0
    negativecount = 0
    alltweet = []
    filteredtweet = []

    for tweet in keyword:
        p = "url"
        imageurl = ""
        co = 1
        ####articles
        if (e == "Article"):
            try:
                p = tweet._json["entities"]["urls"][0]["url"]
            except:
                o = 0
            if (p == "url"):
                continue
        ####
        ####Images
        if (e == "Image"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            y = ""
            try:
                y = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (y != "photo"):
                    co = 0
            except:
                o = 0
        ####
        ####Videos
        if (e == "Video"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            g = ""
            try:
                g = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (g != "video"):
                    co = 0
            except:
                o = 0
        ####
        ####GIF
        if (e == "GIF"):
            try:
                imageurl = tweet._json["extended_entities"]["media"][0]["media_url"]
            except:
                o = 0
            w = ""
            try:
                w = tweet._json["extended_entities"]["media"][0]["type"]
            except:
                o = 0
            try:
                if (w != "animated_gif"):
                    co = 0
            except:
                o = 0
        ####
        if (co == 1):
            PartialWord = ("@", "#", "https", "RT")
            word = tweet.full_text
            wordsplit = word.split(' ')
            wordjoin = [word for word in wordsplit if not word.startswith(PartialWord)]
            word = ' '.join(wordjoin)
            filteredtweet.append(word)
            vs = analyzer.polarity_scores(str(word))
            emoj = [values for key, values in vs.items()]
            emoj = emoj[:-1]
            query = word
            query = np.array(query)
            parser = argparse.ArgumentParser()
            parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
            args = parser.parse_args()

            y = query

            pred = remote.execute(args.url, y)

            y1 = pred.tobytes().decode()

            y = emoj.index(max(emoj))
            mannum = max(emoj)
            # print(vs)
            for tex, num1 in vs.items():
                if num1 == mannum:
                    num1 = round(num1 * 100, 2)
                    valueof = [tex, str(num1)]
                    strvalue = "-".join(valueof)
            if y1 == 'Negative':
                name = 'unamused face'
                negativecount += 1
            elif y1 == 'Neutral':
                name = 'neutral face'
                neutralcount += 1
            elif y1 == 'Positive':
                name = 'grinning face'
                positivecount += 1
            for emoji, name1 in analyzer.make_emoji_dict().items():
                if name1 == name:
                    emoji1 = emoji
            alltweet.append(tweet.full_text)

            '''data = [{'Created at':tweet.created_at},{'Tweet':tweet.full_text.encode('utf-8')},{'Retweet_count':tweet.retweet_count},{'Favourites_count':tweet.user.favourites_count},{'User_name':tweet.user.name.encode('utf-8')},{'Profile_img':tweet.user.profile_image_url},{'Followers_count':tweet.user.followers_count},{'Friends_count':tweet.user.friends_count}]'''
            '''data = [tweet.created_at, tweet.full_text.encode('utf-8'),vs,emoji1,tweet.retweet_count, tweet.user.favourites_count, tweet.user.name.encode('utf-8'), tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count]'''
            # if(e=="Image" or e=="Video" or e=="GIF"):
            data = [tweet.created_at, tweet.full_text, y1, emoji1, tweet.retweet_count, tweet.user.favourites_count,
                    tweet.user.name, tweet.user.profile_image_url, tweet.user.followers_count, tweet.user.friends_count,
                    imageurl]
            ret_data.append(data)
    ####

    ret_data.sort(key=lambda x: x[5])
    ret_data.reverse()

    stringTweet = ','.join(alltweet)

    stopwordsadd = stopwords.words('english')
    stopwordsadd.extend(('RT', '@', ':', '...', '..', '...', '.As', 'dont', 'follow', ',', '#', 'https', '’', 'I', 's',
                         '?', '!', '(', '.', '&', 'amp', ';', "'s", "'", 'It', "n't", '“', '”', '``', "''", '-', ')',
                         '/', 'https…'))

    setstopwords = set(stopwordsadd)
    word_tokens = word_tokenize(stringTweet)

    filtered_sentence = [w for w in word_tokens if not w in setstopwords]

    filtered_sentence = []

    for w in word_tokens:
        if w not in setstopwords:
            filtered_sentence.append(w)

    fdist = FreqDist(filtered_sentence)
    counter = 0
    sample_data = ''
    frequencycount = []
    stringFrequencycount = ''
    for word, frequency in fdist.most_common():
        if len(word) < 10:
            if frequency > 0:
                frequencycount.append(word)
                stringFrequencycount = ','.join(frequencycount)
                if counter < 200:
                    for i in range(0, frequency):
                        sample_data = sample_data + word + ","
                        # final_freq_Dict =sample_data
                    counter = counter + 1

    testlist = [{
        "label": "Positive",
        "value": positivecount
    }, {
        "label": "Neutral",
        "value": neutralcount
    }, {
        "label": "Negative",
        "value": negativecount
    }]

    return (Hashtag_dict, tren, ret_data,
            testlist,
            stringFrequencycount, sample_data)


#################################################################################################
#######################           API SECTION            ########################################
class HelloWorld(Resource):

    def get(self):
        return {'about': 'TwitterAPI Resource'}

    def post(self):
        inputdata = request.get_json()
        keyword1 = inputdata['keyword']

        tweets = inputdata['tweets']
        keyword = tweepy.Cursor(twapi.search, keyword1, tweet_mode='extended', lang='en').items(tweets)
        # keyword = getTweets(keyword1,tweets)
        ret_data = []
        analyzer = SentimentIntensityAnalyzer()
        positivecount = 0
        neutralcount = 0
        negativecount = 0
        alltweet = []
        filteredtweet = []
        for tweet in keyword:
            PartialWord = ("@", "#", "https", "RT")
            word = tweet.full_text
            wordsplit = word.split(' ')
            wordjoin = [word for word in wordsplit if not word.startswith(PartialWord)]
            word = ' '.join(wordjoin)
            filteredtweet.append(word)
            vs = analyzer.polarity_scores(str(word))
            emoj = [values for key, values in vs.items()]
            emoj = emoj[:-1]
            query = word
            query = np.array(query)
            parser = argparse.ArgumentParser()
            parser.add_argument("--url", default="http://127.0.0.1:10000", help="Url", type=str)
            args = parser.parse_args()
            y = query
            pred = remote.execute(args.url, y)

            # d = json.loads(result)
            y1 = pred.tobytes().decode()

            y = emoj.index(max(emoj))
            mannum = max(emoj)
            # print(vs)
            for tex, num1 in vs.items():
                if num1 == mannum:
                    num1 = round(num1 * 100, 2)
                    valueof = [tex, str(num1)]
                    strvalue = "-".join(valueof)
            if y1 == 'Negative':
                name = 'unamused face'
                negativecount += 1
            elif y1 == 'Neutral':
                name = 'neutral face'
                neutralcount += 1
            elif y1 == 'Positive':
                name = 'grinning face'
                positivecount += 1
            for emoji, name1 in analyzer.make_emoji_dict().items():
                if name1 == name:
                    emoji1 = emoji
            alltweet.append(tweet.full_text)
            data = {'tweet created': str(tweet.created_at), 'Full Tweet': tweet.full_text, 'sentiment': y1,
                    'emoji': emoji1, 'retweet count': tweet.retweet_count,
                    'favourite count': tweet.user.favourites_count, 'User name': tweet.user.name,
                    'image': tweet.user.profile_image_url, 'folloer': tweet.user.followers_count,
                    'friend count': tweet.user.friends_count}

            ret_data.append(data)

        return {'Tweet Created': ret_data}, 201
    # return {'Tweet Created':'ret_data'},201



