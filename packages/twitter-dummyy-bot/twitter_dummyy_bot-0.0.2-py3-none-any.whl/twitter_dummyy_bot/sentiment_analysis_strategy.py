#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dotenv import load_dotenv
import os
load_dotenv('.env')

from .strategy_interface import Strategy
from .data_collection import DataCollectionStrategies, DataCollection
from .data_analysis import DataAnalysis
from .resources import GetResource
from .twitter_action import TwitterAction
import emojis

import random


# In[2]:


class SentimentStrategy(Strategy):    
    def __init__(self, number_of_places=1, 
                 trends_range=[2, 4], 
                 tweets_range=[2, 4],
                 top_n_tweets_range=[2, 4],
                 filter_on_english = True):
        
        self.number_of_places = number_of_places
        
        self.number_of_trends = random.randint(*trends_range)
        
        self.number_of_tweets_per_trend = random.randint(*tweets_range)
        
        self.top_n_tweets_per_trend = random.randint(*top_n_tweets_range)
        
        self.analyse_column = random.choice(['retweet_count', 'favorite_count'])

        self.filter_on_english = filter_on_english
        
    def collect(self):
        trends_tweets = DataCollectionStrategies.collect_trends_tweets(
            self.number_of_places, 
            self.number_of_trends,
            self.number_of_tweets_per_trend, 
            self.filter_on_english)
        
        return trends_tweets
        
        
    def analyse(self, collected_data):
        analysed_data = dict()
        # get top n
        for trend in collected_data:
            if isinstance(collected_data[trend], list):
                analysed_data[trend] = []
                continue

            top_n_trend = DataAnalysis.get_top_n(
                collected_data[trend], 
                self.analyse_column, 
                self.top_n_tweets_per_trend)
            
            analysed_data[trend] = DataAnalysis.calculate_sentiment(top_n_trend)
        
        return analysed_data
    
    def behave(self, analysed_data):     
        sentiments_emojis = GetResource().get_sentiment_emojis()
        actions = list()
        for trend in analysed_data:

            if isinstance(analysed_data[trend], list):
                continue
            
            # Itertate over all tweets
            for idx in analysed_data[trend].index:                    
                sent = analysed_data[trend].loc[idx]['sentiment']
                comment = random.choice(sentiments_emojis[sent])
                
                comment = emojis.encode(comment)
                
                params = {
                    'comment': comment,
                    'tweet_from': analysed_data[trend].loc[idx]['author_screen_name'],
                    'tweet_id': analysed_data[trend].loc[idx]['tweet_id_str']
                }
                # append action
                actions.append(TwitterAction('reply', params))
                
        return actions

