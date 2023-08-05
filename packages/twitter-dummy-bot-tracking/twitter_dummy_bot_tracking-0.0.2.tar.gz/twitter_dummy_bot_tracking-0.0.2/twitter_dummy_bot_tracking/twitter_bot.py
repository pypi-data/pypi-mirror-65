#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dotenv import load_dotenv
load_dotenv('.env')

import os
from abc import ABCMeta, abstractmethod
from .twitter_account import TwitterAccountProxy
import random 
import json
import threading
import time

# In[2]:


class TwitterBot:
    def __init__(self,  bot_crediential_file,
        strategy_time_interval_range, action_time_interval_range,
        strategy_class, strategy_params): 
    
        self.bot_account = TwitterAccountProxy(bot_crediential_file)
        self.strategy_time_interval = random.randint(*strategy_time_interval_range)
        self.action_time_interval = random.randint(*action_time_interval_range)
        self.strategy_class = strategy_class
        self.strategy_params = strategy_params
        
    
    def go(self):
        strategy = self.strategy_class(**self.strategy_params)
        actions = strategy.start()
        
        for action in actions:
            # Do action
            self.bot_account.do(action)
            time.sleep(self.action_time_interval * 60)
        
        threading.Timer(self.strategy_time_interval * 3600 , self.go).start()

        