from requests import post


def Twitter_Test():
    print("Result of Twitter keyword search ")
    address = 'http://localhost:5000/twitterdata/twitterAPI'
    tweets = 10

    json_data = {
        'keyword': "twitter",
        'tweets': 2
    }

    resp = post(address, json=json_data).content
    print(resp)

def Text_URL_summary():
    print("Result of URL summarization")
    address = 'http://localhost:5000/textsummarypage/link'
    ratio = 20
    _url = "https://www.lipsum.com/"

    json_data = {
        'url': _url,
        'ratio': ratio
    }

    resp = post(address, json=json_data).content
    print(resp)

def Text_para_summary():
    print("Result of para summarization")
    address = 'http://localhost:5000/textsummarypage/para'
    ratio = 20
    para = "During times of change, many of us find comfort in simple pleasures. Like a great burger. Yet, some of those simple pleasures have been compromised by the dramatic changes caused by COVID-19, including the disruption of the animal meat industry. Meat plants are closing, causing meat to be harder to find and its prices to rise. Some grocers are limiting the amount of meat shoppers can buy to curb pantry loading.I know these issues will be resolved as the pandemic subsides. The animal meat industry will recover, and supply chains will be restored. But right now, you may be asking: What do I do without meat?Now is the time to try plant-based protein. Made from simple ingredients you know, Lightlifeplant-based meat is as nutritious as it is delicious. And you can find the products in your grocer’s meat case.To be clear, I’m not against the animal meat industry. I believe we’re all trying to solve the same complex challenge: how to feed Americans during this pandemic. But I do believe no diet should be entirely dependent on animal meat. That’s why Lightlife is committed to delivering plant-based protein throughout the country to ensure as many people as possible have access to the food they need.At Lightlife, we’re not asking you to give up animal meat. If you want to eat meat, eat meat. But we believe you should also eat plants: whole plants and plant-based protein. That’s why we strive to bring more high-protein options to your table. Fortunately, the trend toward eating more plant-based protein began well before COVID-19, driven by a desire for more balance and variety in our diets, as evidenced by the fact that 44 percent?of Americans now describe themselves as flexitarian.n fact, Lightlife sales were up significantly in the first quarter of 2020. And longer term, the plant-based meat category is expected to grow exponentially, with the Good Food Institute predicting a threefold increase in the number of American households regularly purchasing plant-based protein1.The reality is it takes a little more work these days to make a good burger, even the ones we make with simple ingredients. I want you to know that we’re committed to your dinner table. And your lunch table. And if you want a burger for breakfast, your breakfast table, too.I am so proud of our production teams working around the clock to ensure our products are available at your local grocer. To ensure their health and safety, we have taken additional steps including social distancing wherever possible, daily temperature checks and health screenings, face coverings, increased sanitation efforts, and staggered breaks and start times to reduce the potential for congestion. This is in addition to the sanitation procedures our team is already accustomed to, and the variety of Personal Protective Equipment (PPE) we routinely wear.This is all part of our dedication to getting high-quality, plant-based protein to your tables. Because whether your burger is made from ground beef or plant-based ingredients, a good burger is something we can all agree on. And I believe that together, we will celebrate that simple pleasure once again. 1 The Food Industry Association and IRI. (2020) Understanding the plant-based food consumer."
    json_data = {
        'paragraph': para,
        'ratio': ratio
    }

    resp = post(address, json=json_data).content
    print(resp)


def Text_api_summary():
    print("Result of NewsAPI summarization")
    address = 'http://localhost:5000/textsummarypage/summary'
    resp = post(address).content
    print(resp)



def Senti_URL_summary():
    print("Result of URL summarization")
    address = 'http://localhost:5000/sentimentpage/link'
    ratio = 20
    _url = "https://www.lipsum.com/"

    json_data = {
        'url': _url
    }

    resp = post(address, json=json_data).content
    print(resp)

def Senti_para_summary():
    print("Result of Sentinment summarization")
    address = 'http://localhost:5000/sentimentpage/para'
    ratio = 10
    para = "During times of change, many of us find comfort in simple pleasures. Like a great burger. Yet, some of those simple pleasures have been compromised by the dramatic changes caused by COVID-19, including the disruption of the animal meat industry. Meat plants are closing, causing meat to be harder to find and its prices to rise. Some grocers are limiting the amount of meat shoppers can buy to curb pantry loading.I know these issues will be resolved as the pandemic subsides. The animal meat industry will recover, and supply chains will be restored. But right now, you may be asking: What do I do without meat?Now is the time to try plant-based protein. Made from simple ingredients you know, Lightlifeplant-based meat is as nutritious as it is delicious. And you can find the products in your grocer’s meat case.To be clear, I’m not against the animal meat industry. I believe we’re all trying to solve the same complex challenge: how to feed Americans during this pandemic. But I do believe no diet should be entirely dependent on animal meat. That’s why Lightlife is committed to delivering plant-based protein throughout the country to ensure as many people as possible have access to the food they need.At Lightlife, we’re not asking you to give up animal meat. If you want to eat meat, eat meat. But we believe you should also eat plants: whole plants and plant-based protein. That’s why we strive to bring more high-protein options to your table. Fortunately, the trend toward eating more plant-based protein began well before COVID-19, driven by a desire for more balance and variety in our diets, as evidenced by the fact that 44 percent?of Americans now describe themselves as flexitarian.n fact, Lightlife sales were up significantly in the first quarter of 2020. And longer term, the plant-based meat category is expected to grow exponentially, with the Good Food Institute predicting a threefold increase in the number of American households regularly purchasing plant-based protein1.The reality is it takes a little more work these days to make a good burger, even the ones we make with simple ingredients. I want you to know that we’re committed to your dinner table. And your lunch table. And if you want a burger for breakfast, your breakfast table, too.I am so proud of our production teams working around the clock to ensure our products are available at your local grocer. To ensure their health and safety, we have taken additional steps including social distancing wherever possible, daily temperature checks and health screenings, face coverings, increased sanitation efforts, and staggered breaks and start times to reduce the potential for congestion. This is in addition to the sanitation procedures our team is already accustomed to, and the variety of Personal Protective Equipment (PPE) we routinely wear.This is all part of our dedication to getting high-quality, plant-based protein to your tables. Because whether your burger is made from ground beef or plant-based ingredients, a good burger is something we can all agree on. And I believe that together, we will celebrate that simple pleasure once again. 1 The Food Industry Association and IRI. (2020) Understanding the plant-based food consumer."
    json_data = {
        'paragraph': para
    }
    try:
        resp = post(address, json=json_data).content
    except:
        print ("Network connectivity issue.........")
    print(resp)





Senti_para_summary()

# Text_URL_summary()
# Text_para_summary()
#Text_api_summary()
# Twitter_Test()
