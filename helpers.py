import tweepy
import numpy as np
import pandas as pd
import time
import datetime
import csv
import hashlib
import re
import emoji
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#import seaborn as sns
#import nltk
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud
#from wordcloud import STOPWORDS

def compute_sentiments(df, columns=['text','text_c','text_t', 'text_te'], print_err = False):
    df_out=df.copy()
    analyser = SentimentIntensityAnalyzer()
    
    # Sentiments
    for col in columns:
        lst = list(df[col])

        sents = []
        err = []
        for t in lst:      
            try:
                score = analyser.polarity_scores(t)
                comp = score['compound']
                sents.append(comp)
                err.append(np.nan)
            except Exception as e:
                sents.append(np.nan)
                err.append(e)

        df_out[col+'_sent']=sents

        if print_err:
            df_out[col+'_sent_err']=err

        conditions = [
            (df_out[col+'_sent'] <= -0.05),
            ((df_out[col+'_sent'] > -0.05) & (df_out[col+'_sent'] < 0.05)),
            (df_out[col+'_sent'] >= 0.05)]
        choices = [-1, 0, 1]

        df_out[col+'_stance']= np.select(conditions, choices, default=np.nan)
    
    return df_out

def translate_tweets(df, languages=['en']):
    df_out = df.copy()
    df_out = df_out[['id', 'source', 'author', 'date', 'lang','filter_track', 'text', 'text_c']]
    
    df_out['text_t'] = np.where(df['lang']=='en', df_out['text_c'], '')
                     
#     for t in lst:
#         if any(lang in s for s in languages):
#             text_t = text_c
#         else:
#         trans = translator.translate(text).text
                     
#         Instantiate translator
#         translator = Translator()

#         df_out['text_e'] = handle_emojis(list(df_out['text_c']), 'demojize')
#         translations = translator.translate(list(df_out['text_e']))
    
#         text_t=[]
#         text_lang=[]
#         text_pron=[]    
#         for translation in translations:
#            text_t.append(translation.text)
#            text_lang.append(translation.src)
#            #text_pron.append(translation.pronunciation)
#            #print(translation.origin, ' -> ', translation.text, "\n")
        
#     df_out['text_t'] = text_t
    df_out['text_te'] = handle_emojis(list(df_out['text_t']), 'emojize')
#     df_out['text_lang'] = text_lang
#     #df_out['text_pron'] = text_pron
    
    return df_out	

def handle_emojis(lst, op):
    """
    Handle emojis: 'demojize' or 'emojize'
    """
    
    list_out = []
    for tw in lst:
        if op== 'demojize':
            try:
                list_out.append(emoji.demojize(tw))
            except KeyboardInterrupt:
                pass
            except:
                list_out.append(tw)
                print("An error occured while demojizing: appended untransformed tweet.")
        elif op== 'emojize':
            try:
                list_out.append(emoji.emojize(tw))
            except KeyboardInterrupt:
                pass
            except:
                list_out.append(tw)
                print("An error occured while emojizing: appended untransformed tweet.")
    return list_out

def create_tweet_id(df):
    df_out = df.copy()
 
    author_hash = []
    for tw in df.author:
        author_hash.append(hashlib.md5(tw.encode("utf-8")).hexdigest())
    
    df_out['author_hash'] = author_hash
    df_out['date_hash'] = pd.to_numeric(pd.to_datetime(df.date))
    df_out['tweet_hash'] = df_out['author_hash'].astype(str) + df_out['date_hash'].astype(str)

    tweet_id = []
    for tw2 in df_out.tweet_hash:
        tweet_id.append(hashlib.md5(tw2.encode("utf-8")).hexdigest())

    df_out['tweet_id'] = tweet_id
    df_out = df_out[['tweet_id', 'author', 'date', 'text', 'author_hash', 'date_hash', 'tweet_hash']]

    return df_out

def sentiment_analyzer_scores(text):
    score = analyser.polarity_scores(text)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1

def sentiment_analyzer_scores(text, engl=True):
    if translator.detect(text) == 'en':
        trans = text
    else:
        trans = translator.translate(text).text
    score = analyser.polarity_scores(trans)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1
    
def list_tweets(user_id, count, prt=False):
    tweets = api.user_timeline(
        "@" + user_id, count=count, tweet_mode='extended')
    tw = []
    for t in tweets:
        tw.append(t.full_text)
        if prt:
            print(t.full_text)
            print()
    return tw

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def clean_tweets(df):
    df_out=df.copy()
    df_out=df_out[['id','source','author','date','lang','filter_track','text']]
    lst= df['text']
    # remove twitter Return handles (RT @xxx:)
    lst_RT = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst_handles = np.vectorize(remove_pattern)(lst_RT, "@[\w]*")
    # remove URL links (httpxxx)
    lst_URL = np.vectorize(remove_pattern)(lst_handles, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    lst_punc = np.core.defchararray.replace(lst_URL, "[^a-zA-Z#]", " ")
    lst_nl = np.core.defchararray.replace(lst_punc, "\r\n", " ")
    lst_ws = np.core.defchararray.replace(lst_nl, "[ *]", " ")
    lst_strip = [x.strip() for x in lst_nl]
    lst_em = handle_emojis(lst_strip, 'demojize')
    df_out['text_RT'] = lst_RT
    df_out['lst_handles'] = lst_handles
    df_out['lst_URL'] = lst_URL
    df_out['text_punc'] = lst_punc
    df_out['text_nl'] = lst_nl
    df_out['text_c'] = lst_em
	
    return df_out

def anl_tweets(lst, title='Tweets Sentiment', engl=True ):
    sents = []
    for tw in lst:
        try:
            st = sentiment_analyzer_scores(tw)
            sents.append(st)
        except:
            sents.append(0)
            print(":(")
    ax = sns.distplot(
        sents,
        kde=False,
        bins=3)
    ax.set(xlabel='Negative                Neutral                 Positive',
           ylabel='#Tweets',
          title="Tweets of @"+title)
    return sents

def word_cloud(wd_list):
    stopwords = set(STOPWORDS) #['for', 'and', 'is']
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=1600,
        height=800,
        random_state=21,
        colormap='jet',
        max_words=50,
        max_font_size=200).generate(all_words)
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");

def twitter_stream_listener_extended(auth, file_name,
                            filter_track,
                            follow=None,
                            locations=None,
                            languages=None,
                            time_limit=20, verbose = 1):
	# Tweet-Object attributes: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    class CustomStreamListener(tweepy.StreamListener):
        def __init__(self, time_limit):
            self.start_time = time.time()
            self.limit = time_limit
            # self.saveFile = open('abcd.json', 'a')
            super(CustomStreamListener, self).__init__()
        def on_status(self, status):
            if (time.time() - self.start_time) < self.limit:
                if verbose > 2:
                    print(".", end="")
                # Writing status data
                with open(file_name, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        status.id, status.source, status.author.screen_name, status.created_at, status.lang, status.text#, status.entities.hashtags
                    ])
            else:
                if verbose > 0:
                    print("\n\n[INFO] Closing file and ending streaming")
                return False
        def on_error(self, status_code):
            if status_code == 420:
                print('Encountered error code 420. Disconnecting the stream')
                # returning False in on_data disconnects the stream
                return False
            else:
                print('Encountered error with status code: {}'.format(
                    status_code))
                return True  # Don't kill the stream
        def on_timeout(self):
            print('Timeout...')
            return True  # Don't kill the stream
    # Writing csv titles
    if verbose > 0:
        print(
            '\n[INFO] Open file: [{}] and starting {} seconds of streaming for {}\n'
            .format(file_name, time_limit, filter_track))
    with open(file_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'source', 'author', 'date', 'lang', 'text'])
    streamingAPI = tweepy.streaming.Stream(
        auth, CustomStreamListener(time_limit=time_limit))
    streamingAPI.filter(
        track=filter_track,
        follow=follow,
        locations=locations,
        languages=languages,
    )
    f.close()
    df = pd.read_csv(file_name)
    # this line creates a new column, which is a Pandas series.
    #new_column = df['AUTOWOGEN'] + 1
    # we then add the series to the dataframe, which holds our parsed CSV file
    df['filter_track'] = str(filter_track)
    # save the dataframe to CSV
    df.to_csv(file_name, index=False)
    
def twitter_stream_listener(auth, file_name,
                            filter_track,
                            follow=None,
                            locations=None,
                            languages=None,
                            time_limit=20, verbose = 1):
    class CustomStreamListener(tweepy.StreamListener):
        def __init__(self, time_limit):
            self.start_time = time.time()
            self.limit = time_limit
            # self.saveFile = open('abcd.json', 'a')
            super(CustomStreamListener, self).__init__()
        def on_status(self, status):
            if (time.time() - self.start_time) < self.limit:
                if verbose > 2:
                    print(".", end="")
                # Writing status data
                with open(file_name, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        status.author.screen_name, status.created_at,
                        status.text
                    ])
            else:
                if verbose > 0:
                    print("\n\n[INFO] Closing file and ending streaming")
                return False
        def on_error(self, status_code):
            if status_code == 420:
                print('Encountered error code 420. Disconnecting the stream')
                # returning False in on_data disconnects the stream
                return False
            else:
                print('Encountered error with status code: {}'.format(
                    status_code))
                return True  # Don't kill the stream
        def on_timeout(self):
            print('Timeout...')
            return True  # Don't kill the stream
    # Writing csv titles
    if verbose > 0:
        print(
            '\n[INFO] Open file: [{}] and starting {} seconds of streaming for {}\n'
            .format(file_name, time_limit, filter_track))
    with open(file_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['author', 'date', 'text'])
    streamingAPI = tweepy.streaming.Stream(
        auth, CustomStreamListener(time_limit=time_limit))
    streamingAPI.filter(
        track=filter_track,
        follow=follow,
        locations=locations,
        languages=languages,
    )
    f.close()

def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)
    return hashtags