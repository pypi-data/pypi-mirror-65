import os
import boto3
from dotenv import load_dotenv
import pickle as pk

load_dotenv('.env')


class Setup:
    # Create s3 instance
    s3 = boto3.resource('s3')
    available_actions = ['follow', 'unfollow', 'tweet', 'delete_tweet', 
                         'retweet', 'unretweet', 'like', 'unlike', 'reply',
                         'delete_reply', 'quoted']
    
    def __init__(self, screen_name, strategy_name):       
        # Generate bucket name
        self.bucket_name = f'{screen_name}-{strategy_name}'

        if Setup.s3.Bucket(self.bucket_name).creation_date is None:
            self.create_bot_bucket()
            self.create_actions_logs()

        
    def create_bot_bucket(self):
        # Create a Bucket
        Setup.s3.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'eu-central-1'
    })
        
    def create_actions_logs(self):
        for action in Setup.available_actions:
            loggs = list()

            # Save empty list to each action log
            data = pk.dumps(loggs)
            Setup.s3.Object(self.bucket_name, 
                            f'{action}.pkl').put(Body=data)

