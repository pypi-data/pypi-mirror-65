#!/usr/bin/env python
# coding: utf-8

# In[1]:


from .twitter_object_parsing import TwitterObjectParsing
from .trends_data_collection import Trends
from .twitter_data_collection import QueryTweetsCollector, FavoritedTweetsCollector,UserTimelineTweetsCollector
import pandas as pd

# In[2]:


class DataCollection:
    
    # Collect Data based on keyword
    @staticmethod
    def collect_keyword_tweets(keyword, number_of_tweets, filter_on_english):  
        collector = QueryTweetsCollector(
            DataCollection.query_search_params(keyword)
        )
        
        collector.collect(filter_on_english, number_of_tweets)
        return collector.tweets
        
    # Create Search params dictionary for query search
    @staticmethod
    def query_search_params(keyword):
        search_params = {
            'q': keyword,
            'tweet_mode': 'extended',
            'lang': 'en',
            'include_entities': True,
            'count': 100,  # 100 is the maximum per request (Twitter docs)
            'result_type': 'mixed',
        }
        
        return search_params
    
    # Collect Data favorited by specific user 
    @staticmethod
    def collect_favorited_tweets(user_screen_name, number_of_tweets):  
        collector = FavoritedTweetsCollector(
            DataCollection.favorited_tweet_params(user_screen_name)
        )
        
        collector.collect(number_of_tweets)
        return collector.tweets
    
    # Create Search params dictionary for query search
    @staticmethod
    def favorited_tweet_params(user_screen_name):
        search_params = {
            'id': user_screen_name,
            'tweet_mode': 'extended',
            'lang': 'en',
            'include_entities': True,
            'count': 200   # 200 is the maximum per request(Twitter docs)
        }
        
        return search_params

    # Collect Data form user timeline 
    @staticmethod
    def collect_timeline_tweets(user_id, number_of_tweets):  
        collector = UserTimelineTweetsCollector(
            DataCollection.timeline_tweets_params(user_id)
        )
        
        collector.collect(number_of_tweets)
        return collector.tweets
    
    # Create Search params dictionary for user timeline data
    @staticmethod
    def timeline_tweets_params(user_id):
        search_params = {
            'id': user_id,
            'tweet_mode': 'extended',
            'lang': 'en',
            'include_entities': True,
            'count': 200,   # 200 is the maximum per request (Twitter docs),
            'trim_user': True
        }
        
        return search_params
    
    @staticmethod
    def get_trend_data(number_of_places, filter_on_english):
        # Get trends
        tr = Trends()
        trends_df = tr.get_current_trends_df(filter_on_english, number_of_places=number_of_places)
        
        return trends_df
    
    
    # Convert tweets to data frame
    @staticmethod
    def tweets_list_to_dataframe(tweets):
        parser = TwitterObjectParsing() 
        parsed_tweets = list()
        
        for tw in tweets:
            # Parsing tweet object 
            parsed_tweets.extend(parser.process_tweet_object(tw._json))

        if len(tweets) > 0:
            tweets_df = pd.DataFrame(parsed_tweets)

            # Drop duplicates
            tweets_df.drop_duplicates('tweet_id_str', inplace=True)
        else:
            tweets_df = pd.DataFrame(columns=[
                'author_id_str', 'author_name', 'author_screen_name',
                'created_at', 'favorite_count', 'hashtags', 'lang',
                'location', 'mentions', 'related_screen_name',
                'related_tweet_id_str', 'related_user_id_str', 'retweet_count',
                'source', 'full_text', 'tweet_id_str', 'urls', 'video'])
            
        return tweets_df


# In[3]:


class DataCollectionStrategies:
    @staticmethod
    def collect_trends_tweets(number_of_places, number_of_trends, 
        number_of_tweets, filter_on_english):

        trends_df = DataCollection.get_trend_data(number_of_places, filter_on_english)
        trends_df = trends_df.sort_values(by='tweet_volume', ascending=False)
        trends_df = trends_df[:number_of_trends]
        
        trends_tweets = dict()
        for topic in trends_df.trend_topic:
            trends_tweets[topic] = DataCollection.collect_keyword_tweets(topic, number_of_tweets, 
                filter_on_english)

            if trends_tweets[topic] == []:
                continue

            trends_tweets[topic] = DataCollection.tweets_list_to_dataframe(trends_tweets[topic])
        
        
        return trends_tweets
    
#     @staticmethod
#     def collect_user_favorited_tweets(user_screen_name, number_of_tweets):
#         tweets = DataCollection.collect_favorited_tweets(user_screen_name, number_of_tweets)
#         tweets_df = DataCollection.tweets_list_to_dataframe(tweets)
        
#         return tweets_df
    
#     @staticmethod
#     def collect_user_timeline_tweets(user_id, number_of_tweets):
#         tweets = DataCollection.collect_timeline_tweets(user_id, number_of_tweets)
#         tweets_df = DataCollection.tweets_list_to_dataframe(tweets)
        
#         return tweets_df

