#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dotenv import load_dotenv
import os
load_dotenv('.env')

from .strategy_interface import Strategy
from .data_collection import DataCollectionStrategies, DataCollection
from .data_analysis import DataAnalysis
from .twitter_action import TwitterAction
import botometer
import json
import random


# In[3]:
token_file='twitter_tokens.json'
with open(token_file, 'r') as f:
    token = json.load(f)['twitter_tokens'][0]



class FollowUser(Strategy):
    def __init__(self, number_of_places=1, 
                 trends_range=[2, 4], 
                 tweets_range=[2, 4],
                 top_n_tweets_range=[2, 4],
                 filter_on_english=True,
                 probability_test=0.7,
                 mashape_key ='IJ35CKjQymmshVT1zWpExX38HJgip1TrEu3jsnL3kBNlReJiK5'):
        
        self.number_of_places = number_of_places
        
        self.number_of_trends = random.randint(*trends_range)
        
        self.number_of_tweets_per_trend = random.randint(*tweets_range)
        
        self.top_n_tweets_per_trend = random.randint(*top_n_tweets_range)
        
        self.analyse_column = random.choice(['retweet_count', 'favorite_count'])
        
        self.filter_on_english = filter_on_english

        self.probability_test = probability_test

        self.mashape_key = mashape_key
        
    def collect(self):
        trends_tweets = DataCollectionStrategies.collect_trends_tweets(
            self.number_of_places, 
            self.number_of_trends,
            self.number_of_tweets_per_trend, 
            self.filter_on_english)
        
        return trends_tweets
        
        
    def analyse(self, collected_data):
        analysed_data = dict()
        
        for trend in collected_data:
            analysed_data[trend] = DataAnalysis.get_top_n(
                collected_data[trend], 
                self.analyse_column, 
                self.top_n_tweets_per_trend)
        
        return analysed_data
    
    def behave(self, analysed_data):
        actions_names = ['retweet_', 'like_']
        actions = list()
        for trend in analysed_data:
            action = random.choice(actions_names)

            # Itertate over all tweets
            for idx in analysed_data[trend].index:
                action_ = list()
                # Add the random action
                tweet_id = analysed_data[trend].loc[idx]['tweet_id_str']
                params = {'tweet_id': tweet_id }
                action_.append(TwitterAction(action, params))
                # Get account user probability
                tweet_author = analysed_data[trend].loc[idx]['author_screen_name']
                bom = botometer.Botometer(wait_on_ratelimit=False,
                                  mashape_key=self.mashape_key,
                                  **token)
                result = bom.check_account(tweet_author)

                probability = result['scores']['universal']
                # Test probability and add a follow action depend on the result
                if probability < self.probability_test:

                    params_ = {'user_screen_name': tweet_author}

                    action_.append(TwitterAction('follow_user', params_))
                actions.append(action_)
        return actions


# In[ ]:




