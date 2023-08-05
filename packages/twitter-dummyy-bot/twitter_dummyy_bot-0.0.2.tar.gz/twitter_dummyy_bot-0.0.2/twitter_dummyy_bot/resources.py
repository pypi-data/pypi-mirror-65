#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json


# In[6]:


class GetResource:
    @staticmethod
    def get_sentiment_emojis(resource_file='sentiment_emojis.json'):
        with open(resource_file) as f:
            sentiment_resources = json.load(f)
        return sentiment_resources['emojis']
    
    @staticmethod
    def get_logging_info(resource_file='.logging.json'):
        with open(resource_file) as f:
            logging_info = json.load(f)
        return logging_info
    
    
GetResource.get_logging_info()


# In[ ]:




