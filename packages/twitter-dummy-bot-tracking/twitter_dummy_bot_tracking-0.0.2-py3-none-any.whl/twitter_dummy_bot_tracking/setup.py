from aws_s3_resource.s3_bucket_error import NumberRandomCharsException, NumberCharsBucketNameException
from aws_s3_resource.s3_bucket import S3Bucket
from aws_s3_resource.s3_object import S3Object
import os
import os.path
from os import path
import pickle as pk



class Setup:
    available_actions = ['tweet_delete_events','direct_message_mark_read_events',
                         'direct_message_indicate_typing_events','retweet_to_user_events','retweet_by_user_events',
                         'tweet_create_events','reply_to_user_events','reply_by_user_events',
                         'mention_to_user_events','message_to_user_events','message_by_user_events','follow_to_user_events','follow_by_user_events',
                         'unfollow_by_user_events','block_by_user_events','unblock_by_user_events','mute_by_user_events',
                         'unmute_by_user_events','favorite_to_user_events','favorite_by_user_events']
    
    def __init__(self, storing_medium, events_folder = None, bucket_name = None):
        # Setup bucket on s3 or local folder according to storing_medium
        if storing_medium == 's3':
            if not S3Bucket.is_available(bucket_name):
                self.bucket_name = bucket_name
                self.create_bot_bucket()
                self.create_actions_logs()
        else:
            if not path.exists(events_folder):
                self.events_folder = events_folder
                self.create_events_folder()
                self.create_events_log_files()




    def create_bot_bucket(self):
        # Create a Bucket
        S3Bucket.create(self.bucket_name)
        
    def create_actions_logs(self):
        for action in Setup.available_actions:
            loggs = list()

            # Save empty list to each action log
            file_dict = {
                'file_name': f'{action}.pkl',
                'file_bytes': pk.dumps(loggs)
            }
            
            S3Object.upload(self.bucket_name, file_dict, with_random_prefix=False)

    def create_events_folder(self):
        os.mkdir(self.events_folder)

    def create_events_log_files(self):
        for action in Setup.available_actions:
            loggs = list()
            with open(os.path.join(self.events_folder, f'{action}.pkl'), 'wb') as f:
                pk.dump(loggs, f)
