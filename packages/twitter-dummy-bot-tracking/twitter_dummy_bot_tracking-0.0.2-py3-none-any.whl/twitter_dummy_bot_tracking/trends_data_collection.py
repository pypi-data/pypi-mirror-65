#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import tweepy
import pandas as pd
import numpy as np
import pickle as pk
import json
from .twitter_api_preparation import TwitterAPI
from .twitter_data_collection import TweetsCollector, DataCollector
from abc import ABCMeta, abstractmethod
from langdetect import detect
# from yahoo_api import YahooAPI


# In[2]:


class TrendsCollector(metaclass=ABCMeta):
    """ This class is an abstract class to collect trends topics and trends places """
    def __init__(self, columns_to_be_dropped=[], col_names_to_be_changed=dict()):
        self.data_df = None
        self.columns_to_be_dropped = columns_to_be_dropped
        self.col_names_to_be_changed = col_names_to_be_changed
    
    @abstractmethod
    def request_data(self):
        pass
    
    def fix_some_columns(self):
        pass
    
    def rename_some_columns(self):
        self.data_df.rename(self.col_names_to_be_changed, inplace=True, axis=1)
    
    def drop_some_columns(self):
        self.data_df.drop(self.columns_to_be_dropped, inplace=True, axis=1)
    
    def add_some_columns(self):
        pass


# In[3]:


class TrendsPlaces(TrendsCollector):
    """ This class is responsible for getting the trends places from the twtiiter API """
    
    def __init__(self):
        super().__init__(['url', 'parentid', 'place_code'], 
                         {
                             'name': 'place_name',
                             'countryCode': 'country_code'
                         })
        
    def get_data_df(self, number_of_places):
        self.request_data(number_of_places)
        self.fix_some_columns()
        self.rename_some_columns()
        self.drop_some_columns()
        self.add_some_columns()
        
        return self.data_df
    
    def request_data(self, number_of_places):
        """ Get the list of trends places from Twitter API """
        ta = DataCollector.trends_available_collector()
        trends_places = ta.get()
        self.data_df = pd.DataFrame(trends_places[:number_of_places])
    
    def fix_country_code_col(self):
        """ Put each None in countryCode as Worldwide """
        self.data_df['countryCode'] = self.data_df['countryCode'].apply(
                                        lambda x: 'Worldwide' if x is None else x)
        
    def fix_country_col(self):
        """ Put each None in country as Worldwide """
        self.data_df['country'] = self.data_df['country'].apply(
                                        lambda x: 'Worldwide' if x is '' else x)
        
    def fix_place_type_col(self):
        """ Convert the place_type dict into two columns in the dataframe """
        
        pt = self.data_df.pop('placeType')
        pt_df = pd.DataFrame(pt.values.tolist(), index = self.data_df.index)
        pt_df.columns = ['place_code', 'place_type']
        self.data_df = self.data_df.join(pt_df)
    
    def fix_some_columns(self):
        self.fix_country_code_col()
        self.fix_country_col()
        self.fix_place_type_col()
    
    def get_woeids_list(self):
        return self.data_df.woeid.values.tolist()
    
    def add_woeid_places_coordinates(self):
        """ Get actual coordinates for each place using Yahoo API """
        
        woeids_list = self.get_woeids_list()
        coords_list = []
#         yahoo_api = YahooAPI()
        for woeid in woeids_list:
            coord = {'long': 0, 'lat': 0} # yahoo_api.get_lng_lat(woeid)  # TODO
            coords_list.append(coord)
        
        coords_df = pd.DataFrame(coords_list)
        self.data_df = self.data_df.join(coords_df)
    
    def add_some_columns(self):
        self.add_woeid_places_coordinates()


# In[4]:


class TrendsTopics(TrendsCollector):
    """ This class is responsible for getting the trends topics from the twtiiter API """
    def __init__(self, woeids_list, filter_on_english=True):
        super().__init__(['promoted_content', 'query'],
                       {
                           'url': 'trend_twitter_url',
                           'name': 'trend_topic'
                       })
        self.woeids_list = woeids_list
        self.filter_on_english = filter_on_english
    
    def get_data_df(self):
        self.request_data()
        self.fix_some_columns()
        self.rename_some_columns()
        self.drop_some_columns()
        self.add_some_columns()
        
        return self.data_df
    
    def request_data(self):
        """ Get the trends for each place """
        tp = DataCollector.trends_place_collector()
        trends_topics = list()

        for woeid in self.woeids_list:
            # Get the trends
            trends = tp.get(woeid)
            
            # Get trends place id only
            location = trends[0]['locations'][0]
            location.pop('name')
            
            # Merge id with the trends
            if self.filter_on_english:
                trends = [{**trnd, **location} for trnd in trends[0]['trends'] if detect(trnd['name']) == 'en']

            else:
                trends = [{**trnd, **location} for trnd in trends[0]['trends']]
            
            # Add to the topics list
            trends_topics.extend(trends)
            
        # Create a dataframe for the whole world trends
        self.data_df = pd.DataFrame(trends_topics)
                
        return self.data_df


# In[5]:


class Trends:
    """ This class is responsible for getting the trends places and topics from 
        the twtiiter API 
    """
    def __init__(self):
        self.trends_places_df = None
        self.trends_topics_df = None
        self.trends_df = None
    
    def get_current_trends_df(self, filter_on_english, number_of_places=10):
        # Get trends places dataframe
        print('Get trends places .. ')
        tr_pl = TrendsPlaces()
        self.trends_places_df = tr_pl.get_data_df(number_of_places)
        
        # Get trends topics dataframe
        print('Get trends topics .. ')
        tr_tp = TrendsTopics(tr_pl.get_woeids_list(), filter_on_english=filter_on_english)
        self.trends_topics_df = tr_tp.get_data_df()
        
        print('Merging')
        # Create the full trends dataframe
        self.trends_df = self.trends_topics_df.merge(self.trends_places_df, how='left', 
                                                     left_on='woeid', right_on='woeid')
        
        Trends.convert_nan_to_none(self.trends_df, 'tweet_volume')
        return self.trends_df
        
    @staticmethod
    def convert_nan_to_none(df, key):
        df[key] = df[key].where(pd.notnull(df[key]), None)


# In[6]:


# # %%time
# tr = Trends()
# tr.get_current_trends_df()


# In[ ]:




