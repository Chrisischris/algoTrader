#Queries tweets by twitter handle

import sys
import json
import tweepy 
import csv
import re
from auth.twitter_auth import *


def get_all_tweets_user(screen_name, api):    
      
    alltweets = []  
    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    with open(f'new_{screen_name}_tweets.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(outtweets)
    
    pass


def get_all_tweets_keyword(keyword, api):
    fname = '_'.join(re.findall(r"#(\w+)", keyword))
    
    with open('%s.csv' % (fname), "wb") as file:
        w = csv.writer(file)
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

    tweet_count = input("How many tweets would you like to query?")

    for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', \
                                   lang="en", tweet_mode='extended').items(tweet_count):
            w.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), 
            tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], 
            tweet.user.followers_count])

def main():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    if len(sys.argv != 2):
        print("Usage: query_twitter.py keyword/userhandle")
        return

    if sys.argv[1] == "userhandle":

        while True:
            name = input("Input Twitter handle to search for user's tweets(tilde(~) to quit): ")
            if name == "~":
                return
            else:
                get_all_tweets_user(name, api)

    elif sys.argv[1] == "keyword":
    
        while True:
            keyword = input("Input keyword to search for user's tweets(tilde(~) to quit): ")
            if keyword == "~":
                return
            else:
                get_all_tweets_user(keyword, api)
    else:
        print("Usage: query_twitter.py keyword/userhandle")
        return


if __name__ == '__main__':
    main()