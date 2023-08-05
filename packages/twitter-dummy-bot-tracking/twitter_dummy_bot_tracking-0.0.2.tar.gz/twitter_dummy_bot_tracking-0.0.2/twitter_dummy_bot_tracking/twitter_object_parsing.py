#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import datetime
import html


# In[2]:


class TwitterObjectParsing:  
    # Parsing tweet object
    def process_tweet_object(self, tweet_json):       
        # Retweet 
        if 'retweeted_status' in tweet_json:
            return self.__parse_retweeted_tweet(tweet_json)
    
        # Quote  
        if tweet_json['is_quote_status']:
            return self.__parse_quoted_tweet(tweet_json)
        
        # Reply 
        if tweet_json['in_reply_to_status_id'] is not None:
            return self.__parse_reply_tweet(tweet_json)

        # Tweet 
        return self.__parse_tweet(tweet_json)
    
    def __extract_hashtags(self, status_text):
        """ Extract hashtags from a string """
        hashtags = re.findall(r"#\w+", status_text)
        return list(set([h.lower() for h in hashtags]))
    
    def __extract_mentions(self, status_text):
        """ Extract mentions from a string """
        mentions = re.findall(r"@\w+", status_text)
        return list(set([m.lower() for m in mentions]))
    
    def __remove_media_urls (self, status_text, media_url):
        """Remove Media URLs from text (photos, video, gif), 
        twitter adds media url by default""" 
        return status_text.replace(media_url, "")
    
    def __remove_appended_url(self, tweet_text):
        """Remove quoted status URL from tweet text 
        (Twitter adds quoted status URL  at the end of tweet text by defualt)"""
        return re.sub(r'(https?:\/\/t\.co/\w+)$', '', tweet_text)
    
    def __remove_status_urls(self, urls_list):
        # Remove status URL from URLs list(Twitter adds quoted tweet link to the quote text)
        return [u for u in urls_list
                  if 'https://twitter.com' not in u and 'status' not in u]
    
    def __parse_created_at_date(self, input_date):
        # Use re to get rid of the milliseconds.
        input_date = re.sub("\+\d+\s","", input_date)

        # Convert the string into datetime object
        output_date = datetime.datetime.strptime(input_date, "%a %b %d %H:%M:%S %Y")
        
        return output_date
    
    def __parse_tweet_coordinates(self, coordinates, coord_type):
        """ This function extracts the coordinates from the tweet object """

        # Check the coordinates format
        if coordinates['type'] == 'Point':
            # Take the value directly
            crds = coordinates['coordinates']

        elif coordinates['type'] == 'Polygon':
            # Take the average over the four points
            crds = np.array(coordinates['coordinates'][0]).mean(axis=0)
        
        else:
            crds = [None, None]

        # Check if they come from the field 'coordinates' or 'geo'
        if coord_type == 'coordinates':
            long, lat = crds[0], crds[1]

        elif coord_type == 'geo':
            long, lat = crds[1], crds[0]
        else:
            long, lat = None, None

        return long, lat
    
    def __parse_basic_tweet(self, tweet_json, tweet_type = 't', come_from = 'o',
        # Create a basic form of tweet and parse it
                          related_screen_name = None,
                          related_user_id_str = None,
                          related_tweet_id_str = None):

        # tweet_type could be: t - rt - rp - q
        # come_from could be: o - rt - q

        tweet = dict()

        # Main details
        tweet['tweet_type'] = tweet_type
        tweet['created_at'] = self.__parse_created_at_date(
            tweet_json['created_at'])
        tweet['lang'] = tweet_json['lang']
        tweet['author_screen_name'] = tweet_json['user']['screen_name'].lower()
        tweet['author_name'] = tweet_json['user']['name']
        tweet['author_id_str'] = tweet_json['user']['id_str']
        tweet['tweet_id_str'] = tweet_json['id_str']
        tweet['source'] = re.findall('>(.+)<', tweet_json['source'])[0]

        # Statistics
        tweet['retweet_count'] = tweet_json['retweet_count']
        tweet['favorite_count'] = tweet_json['favorite_count']

        # Relationship
        tweet['come_from'] = come_from
        tweet['related_screen_name'] = related_screen_name#.lower() if related_screen_name is not None else None
        tweet['related_user_id_str']  = related_user_id_str
        tweet['related_tweet_id_str'] = related_tweet_id_str

        # Text and entities (Will be filled according to the case)
        tweet['text'] = None 
        tweet['urls'] = None
        tweet['hashtags'] = None
        tweet['mentions'] = None
        tweet['photo'] = None
        tweet['video'] = None
        tweet['animated_gif'] = None
        
        return tweet
        
    def __update_tweet(self, tweet_json):
        # Update the tweet

        tweet = dict()
        # Original text
        tweet['text'] = html.unescape(tweet_json['full_text'])
        
        if 'media' in tweet_json['entities'].keys():     # Remove media url in tweet        
            # Remove the url from the tweet text
            tweet['text'] = self.__remove_media_urls(tweet['text'],
                            tweet_json['entities']['media'][0]['url'])
            
            # Add media URL to it's column
            tweet[tweet_json['extended_entities']['media'][0]['type']] = tweet_json[
                'extended_entities']['media'][0]['expanded_url']

        tweet['urls'] = [u['expanded_url'] for u in tweet_json['entities']['urls']]
        tweet['hashtags'] = self.__extract_hashtags(tweet_json['full_text'])
        tweet['mentions'] = self.__extract_mentions(tweet_json['full_text'])

        return tweet
    
    def __parse_tweet(self, tweet_json, tweet_type = 't', come_from = 'o',
                        related_screen_name = None,
                        related_user_id_str = None,
                        related_tweet_id_str = None):
        
        """ Parse the normal tweet"""
        tweet = self.__parse_basic_tweet(tweet_json, tweet_type, come_from,
                          related_screen_name, related_user_id_str, related_tweet_id_str)
        
        tweet.update(self.__update_tweet(tweet_json))
        return [tweet]
    
    def __parse_reply_tweet(self, tweet_json, come_from = 'o' , tweet_type = 'rp'):
        """ Parse Reply tweet (it's like normal but differ in some reply info) """
        return self.__parse_tweet(tweet_json, tweet_type = tweet_type , come_from = come_from,
                          related_screen_name = tweet_json['in_reply_to_screen_name'].lower(),
                          related_user_id_str = tweet_json['in_reply_to_user_id_str'],
                          related_tweet_id_str = tweet_json['in_reply_to_status_id_str'])
    
    
    def __parse_retweeted_tweet(self, tweet_json):         
        """ Parse retweet and retweeted tweet """

        # Parse the retweeted tweet
        if tweet_json['retweeted_status']['in_reply_to_status_id'] is not None: 
            # If retweeted tweet is reply
            retweeted_tweet = self.__parse_reply_tweet(
                tweet_json['retweeted_status'], come_from = 'rt')
        
        elif tweet_json['retweeted_status']['is_quote_status']:
            retweeted_tweet = self.__parse_quoted_tweet(
                tweet_json['retweeted_status'], come_from = 'rt')
            
        else:   # If retweeted tweet is a normal tweet (Retweet to Normal)
            retweeted_tweet = self.__parse_tweet(
                tweet_json['retweeted_status'], come_from = 'rt')

        # Parse the retweet, assign to it same info of retweeted tweet.
        tweet = self.__parse_basic_tweet(tweet_json, tweet_type = 'rt',
                            related_screen_name = retweeted_tweet[0]['author_screen_name'].lower(),
                            related_user_id_str = retweeted_tweet[0]['author_id_str'],
                            related_tweet_id_str = retweeted_tweet[0]['tweet_id_str'])
        
        # Media
        tweet['photo'] = retweeted_tweet[0]['photo']
        tweet['video'] = retweeted_tweet[0]['video']
        tweet['animated_gif'] = retweeted_tweet[0]['animated_gif']
        
        # Text text
        tweet['text'] = retweeted_tweet[0]['text']
        
        # Entities
        tweet['hashtags'] = retweeted_tweet[0]['hashtags']
        tweet['mentions'] = retweeted_tweet[0]['mentions']
        tweet['urls'] = retweeted_tweet[0]['urls']
        
        # Interactions
        tweet['retweet_count'] = retweeted_tweet[0]['retweet_count'] 
        tweet['favorite_count'] = retweeted_tweet[0]['favorite_count'] 
        
        return [tweet, *retweeted_tweet]
    
    def __parse_quoted_tweet(self, tweet_json, come_from='o'):
        """ Parse quoted tweet and the quote """

        # Parse the quoted tweet
        if 'quoted_status' not in tweet_json:
            # Quoted tweet is not avaliable
            return self.__parse_tweet(tweet_json, tweet_type='q', come_from=come_from)
        else:  
            # Quoted tweet is avaliable
            
            if tweet_json['quoted_status']['in_reply_to_status_id'] is not None:
                # If quoted tweet is reply tweet (quote to reply case)
                quoted_tweet = self.__parse_reply_tweet(
                    tweet_json['quoted_status'], come_from='q')[0]

            elif tweet_json['quoted_status']['is_quote_status']:
                # If the quoted tweet is a quote(quote to quote case)
                
                quoted_tweet = self.__parse_tweet(
                    tweet_json['quoted_status'], tweet_type='q', come_from='q')[0]

                quoted_tweet['urls'] = self.__remove_status_urls(quoted_tweet['urls'])
                quoted_tweet['text'] = self.__remove_appended_url(quoted_tweet['text'])
            else:  
                # The quoted tweet is normal tweet
                quoted_tweet =self.__parse_tweet(
                    tweet_json['quoted_status'], come_from='q')[0]

            # Parse the quote
            tweet = self.__parse_tweet(tweet_json, tweet_type='q', come_from=come_from,
                                related_screen_name=quoted_tweet['author_screen_name'],
                                related_user_id_str=quoted_tweet['author_id_str'],
                                related_tweet_id_str=quoted_tweet['tweet_id_str'])[0]

            # Remove root URL from enduser text
            tweet['text'] = self.__remove_appended_url(tweet['text'])

            tweet['hashtags'] = list(set(tweet['hashtags'] + quoted_tweet['hashtags']))
            tweet['mentions'] = list(set(tweet['mentions'] + quoted_tweet['mentions']))
            
            tweet['photo'] = quoted_tweet['photo']
            tweet['video'] = quoted_tweet['video']
            tweet['animated_gif'] = quoted_tweet['animated_gif']

            # Remove the quote tweet url (Auto added by twitter)
            tweet['urls'] = self.__remove_status_urls(tweet['urls'])
            tweet['urls'] = list(set(tweet['urls'] + quoted_tweet['urls']))

            return [tweet, quoted_tweet]

