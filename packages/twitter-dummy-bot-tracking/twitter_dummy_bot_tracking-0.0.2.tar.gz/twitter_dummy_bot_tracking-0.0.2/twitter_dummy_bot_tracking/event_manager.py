import pickle as pk
import os
import io
from aws_s3_resource.s3_bucket import S3Bucket
from aws_s3_resource.s3_object import S3Object
from .setup import Setup
import time 


class EventManager:
    """ This class works on determine events and save them as local or s3 storing_medium """
    basic_events = ['tweet_delete_events', 'direct_message_mark_read_events',
                    'direct_message_indicate_typing_events']

    type_based_events = ['follow_events','mute_events','block_events']

    # Conditons to determine who did the event
    by_to_conditions = {
        'by_if_equal': lambda id1, id2: 'by' if id1 == id2 else 'to',
        'to_if_equal': lambda id1, id2: 'to' if id1 == id2 else 'by'
    }
    
    def __init__(self, storing_medium='local', events_folder=os.getcwd(), bucket_name = None):
        # Call setup function , define save event functions according to storing_medium
        if storing_medium == 'local':
            self.events_folder = events_folder
            Setup(storing_medium=storing_medium, events_folder=events_folder)
            self.save_func = self.save2pickle

        elif storing_medium == 's3':
            self.bucket_name = bucket_name
            Setup(storing_medium=storing_medium, bucket_name=bucket_name)
            self.save_func = self.save2s3

    # Svae event to S3
    def save2s3(self, pickle_name, response):
        object_key  = f'{pickle_name}.pkl'
        logg_bytes = S3Object.download(self.bucket_name, object_key)

        with io.BytesIO(logg_bytes) as f:
            loggs = pk.load(f)

        action = {f'{pickle_name}' : response}

        # Add current action to log
        action['timestamp'] = int(time.time())
        loggs.append(action)

        data_bytes = pk.dumps(loggs)

        file_dict = {
            'file_name': object_key,
            'file_bytes': data_bytes
        }

        S3Object.upload(self.bucket_name, file_dict, with_random_prefix=False)
        return f'successful {pickle_name}'

    # Svae event to pickle file
    def save2pickle(self, pickle_name, response):
      with open(os.path.join(self.events_folder, f'{pickle_name}.pkl'), 'rb') as f:
          events = pk.load(f)

      events.append(response)

      with open(os.path.join(self.events_folder, f'{pickle_name}.pkl'), 'wb') as f:
          pk.dump(events, f)

      return f'successful {pickle_name}'

    def save_events(self, response):
        # Get events list
        keys_list = response.keys()

        # Get event name
        event_name = self.get_activity_name(keys_list)

        if event_name in EventManager.basic_events:
            pickle_name = event_name

        else:
            # If event depends on type 
            if event_name in EventManager.type_based_events:

                # Get event type
                event_type = response[f'{event_name}'][0]['type']

                # Test if the event done by user or to user 
                if event_type == 'follow':
                    follow_to = response['follow_events'][0]['target']['id']
                    user_id = response['for_user_id']
                    res = EventManager.by_to_conditions['to_if_equal'](user_id, follow_to)
                    pickle_name = f'follow_{res}_user_events'

                # if event is unfollow, mute, unmute, block, or unblock
                else:
                    pickle_name = f'{event_type}_by_user_events'

            elif event_name == 'direct_message_events':
                message_by = response["direct_message_events"][0]['message_create']['sender_id']
                user_id = response['for_user_id']
                res = EventManager.by_to_conditions['by_if_equal'](message_by, user_id)
                pickle_name = f'message_{res}_user_events'

            elif event_name == 'favorite_events':
                favorite_by = response['favorite_events'][0]['user']['id_str']
                user_id = response['for_user_id']
                res = EventManager.by_to_conditions['by_if_equal'](favorite_by, user_id)
                pickle_name = f'favorite_{res}_user_events'

            elif event_name == 'tweet_create_events':
                # tweet create events maybe tweet (by user), retweet(to user,by user) , reply(to user,by user),mention (to user)
                if response['tweet_create_events'][0]['in_reply_to_status_id'] is None:
                   # just to recocnize is it retwee or tweet by user
                   # if no it is tweet event
                    if "retweeted_status" in response['tweet_create_events'][0].keys():
                        retweeted_by = response['tweet_create_events'][0]['user']['id_str']
                        user_id = response['for_user_id']

                        res = EventManager.by_to_conditions['by_if_equal'](retweeted_by, user_id)
                        pickle_name = f'retweet_{res}_user_events'

                    else:
                        pickle_name = event_name

                else:

                    if response['tweet_create_events'][0]['in_reply_to_user_id_str'] == response['for_user_id']:
                        pickle_name = 'reply_to_user_events'

                    else:
                        if response['tweet_create_events'][0]['user']['id_str'] == response['for_user_id']:
                            pickle_name = 'reply_by_user_events'
                        else:
                            pickle_name = 'mention_to_user_events'


        return self.save_func(pickle_name, response)

    def get_activity_name(self, keys_list):
        for k in keys_list:
            if 'event' in k:
                return k