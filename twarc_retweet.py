#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 22:45:43 2020

@author: ashutosh
"""


from twarc import Twarc
import json
import codecs
consumer_key="o1WMn7KyuJsHxduqUATrNuLK3"
consumer_secret="4AWb6rVPY2JkZZOuaIBmyTnfqucYsJeiXL8rNEUMu1QH9rgnmm"
access_token="917696760276852742-JvOeDr8rOBLwe2P0nkYXRm2xu3HcUcb"
access_token_secret="FjLugXVJrzHBwuNZN3DjoOMEHqh2D1Z5MMq4NB0Z4WWW6"
# This creates an instance of Twarc.
t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

# Create a summary of a tweet, only showing relevant fields.
def summarize(tweet, extra_fields = None):
    new_tweet = {}
    for field, value in tweet.items():
        if field in ["text", "id_str", "screen_name", "retweet_count", "favorite_count", "in_reply_to_status_id_str", "in_reply_to_screen_name", "in_reply_to_user_id_str"] and value is not None:
            new_tweet[field] = value
        elif extra_fields and field in extra_fields:
            new_tweet[field] = value
        elif field in ["retweeted_status", "quoted_status", "user"]:
            new_tweet[field] = summarize(value)
    return new_tweet


# Print out a tweet, with optional colorizing of selected fields.
def dump(tweet, colorize_fields=None, summarize_tweet=True):
    colorize_field_strings = []
    
    for line in json.dumps(summarize(tweet) if summarize_tweet else tweet, indent=4, sort_keys=True).splitlines():
        colorize = False
        for colorize_field in colorize_fields or []:
            if "\"{}\":".format(colorize_field) in line:  
                print("\x1b" + line + "\x1b"+"\n")
                break
        else:
            print(line+"\n")
            
# collect tweet_id from t_id.txt file
def ids():
    for id in open("t_id.txt"):
        yield id

#find retweets, reply, quotes for each tweet_id
for tweet in t.hydrate(ids()):
    dump(tweet, colorize_fields=['retweeted_status', 'retweet_count','quoted_status_id', 'quoted_status_id_str','in_reply_to_status_id_str', 'in_reply_to_user_id'])
          
