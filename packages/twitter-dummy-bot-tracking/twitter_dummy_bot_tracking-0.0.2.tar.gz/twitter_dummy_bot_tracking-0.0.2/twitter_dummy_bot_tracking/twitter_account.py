
import tweepy
from pprint import pprint
import random
import json
import time
import pickle as pk
from .twitter_action import TwitterAction
from botocore.exceptions import ClientError
import io



# In[2]:


class TwitterAccountProxy(tweepy.API):

    def __init__(self,
        token_file='twitter_tokens.json', wait_on_rate_limit=False,
        timeout=10, retry_count=3):


        # Dictionary contains twitter application keys
        with open(token_file, 'r') as f:
            self.token = json.load(f)['twitter_tokens'][0]
                
        auth = tweepy.OAuthHandler(self.token['consumer_key'],
                                   self.token['consumer_secret'])
        
        auth.set_access_token(self.token['access_token'],
                              self.token['access_token_secret'])
        
        # Call tweepy.API to create api object
        super().__init__(auth, wait_on_rate_limit=wait_on_rate_limit,
                         timeout=timeout, retry_count=retry_count)
        
    @staticmethod
    def follow_user(self, user_screen_name):
        # user_screen_name could be either screen name or user id
        self.create_friendship(user_screen_name)


    def unfollow_user(self, user_screen_name):
        # user_screen_name could be either screen name or user id
        self.destroy_friendship(user_screen_name)

    def block_user (self,user_screen_name):
        # user_screen_name could be either screen name or user id
        self.create_block (user_screen_name)

    def unblock_user(self,user_screen_name):
        # user_screen_name could be either screen name or user id
        self.destroy_block(user_screen_name)

    def mute_user(self,user_screen_name):
        # user_screen_name could be either screen name or user id
        self.create_mute(user_screen_name)

    def unmute_user(self,user_screen_name):
        # user_screen_name could be either screen name or user id
        self.destroy_mute(user_screen_name)


    def tweet(self, tweet_text):
        self.update_status(tweet_text)

    def delete_tweet(self, tweet_id):
        deleted_tweet = self.get_status(tweet_id)
        
        self.destroy_status(tweet_id)


        
    def retweet_(self, tweet_id):
        self.retweet(tweet_id)

    def unretweet_(self, tweet_id):
        unretweeted_tweet = self.get_status(tweet_id)
        
        self.unretweet(tweet_id)
        
    def like_(self, tweet_id):
        self.create_favorite(tweet_id)

    def unlike(self, tweet_id):
        self.destroy_favorite(tweet_id)


    def reply(self, comment, tweet_from, tweet_id):
        # Reply should have screen name of who you want to reply to and the tweet you want to reply on
        self.update_status(f'{comment} @{tweet_from}', in_reply_to_status_id=tweet_id, 
            auto_populate_reply_metadata=True)
        
        # logging
        reply_to = self.get_status(tweet_id)
        

    def delete_reply(self, tweet_id):
        self.delete_tweet(tweet_id)

    def quoted_tweet(self, comment, tweet_from, tweet_id):
        # Quoted tweet is ordinary tweet with another tweet link and comment 
        tweet_url = f'https://twitter.com/{tweet_from}/status/{tweet_id}'
        
        self.update_status(f'{comment} \n {tweet_url}')


    def send_message(self,recipient_id,message_text):
        self.send_direct_message(recipient_id,message_text)

    def do(self, action):
        try:
            eval(f"self.{action.name}(**{action.params})")

        except:
            pass
            


