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
import emojis
#from .resources import GetResource
from datetime import datetime
import random


# In[3]:


class ActionStrategy(Strategy):
    def __init__(self, number_of_places=1, 
                 trends_range=[2, 4], 
                 tweets_range=[2, 4],
                 top_n_tweets_range=[2, 4],
                 filter_on_english=True ,
                 tweet = str(datetime.now()),
                 comment = 'just test comment',
                 recipient_id_str = "1027079038446260224",
                 message_text = 'hello bro/sis'
                 ):
        
        self.number_of_places = number_of_places
        
        self.number_of_trends = random.randint(*trends_range)
        
        self.number_of_tweets_per_trend = random.randint(*tweets_range)
        
        self.top_n_tweets_per_trend = random.randint(*top_n_tweets_range)
        
        self.analyse_column = random.choice(['retweet_count', 'favorite_count'])
        
        self.filter_on_english = filter_on_english
        self.tweet = tweet
        self.comment = comment
        self.recipient_id_str= recipient_id_str
        self.message_text = message_text
        
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
        actions_names = ['retweet_', 'like_','follow_user','unfollow_user','delete_tweet','unretweet_',
                         'unlike','delete_reply','reply','tweet' , 'quoted_tweet',
                         'block_user','unblock_user','mute_user','unmute_user','send_message']
        actions = list()
        for trend in analysed_data:
            action = random.choice(actions_names)
            # Itertate over all tweets
            for idx in analysed_data[trend].index:
                user_related_actions = ['follow_user','unfollow_user','block_user','unblock_user','mute_user','unmute_user']
                if action in user_related_actions :
                    user_screen_name = analysed_data[trend].loc[idx]['author_screen_name']
                    params = {'user_screen_name': user_screen_name}
                    # append action
                    actions.append(TwitterAction(action, params))

                elif action == 'reply':
                    comment = self.comment

                    params = {
                        'comment': comment,
                        'tweet_from': analysed_data[trend].loc[idx]['author_screen_name'],
                        'tweet_id': analysed_data[trend].loc[idx]['tweet_id_str']
                    }
                    # append action
                    actions.append(TwitterAction('reply', params))

                elif action == 'tweet':
                    tweet = self.tweet
                    params = {'tweet_text' : tweet}
                    # append action
                    actions.append(TwitterAction('tweet', params))

                elif action == 'quoted_tweet':
                    comment = self.comment

                    params = {
                        'comment': comment,
                        'tweet_from': analysed_data[trend].loc[idx]['author_screen_name'],
                        'tweet_id': analysed_data[trend].loc[idx]['tweet_id_str']
                    }
                    # append action
                    actions.append(TwitterAction('quoted_tweet', params))

                elif action == 'send_message':
                    recipient_id = self.recipient_id_str
                    message_text = self.message_text
                    params = {'recipient_id' :recipient_id , 'message_text' : message_text}
                    # append action
                    actions.append(TwitterAction('send_message', params))
                else:
                    tweet_id = analysed_data[trend].loc[idx]['tweet_id_str']
                    params = {'tweet_id': tweet_id}
                    actions.append(TwitterAction(action, params))

        return actions


# In[ ]:




