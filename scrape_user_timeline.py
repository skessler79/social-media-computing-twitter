import tweepy
from tweepy import OAuthHandler
import pandas as pd
import json
import config

# Change this
# USERNAME = "TheBabylonBee"
# USERNAME = "HardDriveMag"
# USERNAME = "Reductress"
USERNAME = "TheOnion"

def get_tweets(api, username, count=200, oldest_id=-1):
    if oldest_id == -1:
        tweets = api.user_timeline(screen_name=username, count=count)
    else:
        tweets = api.user_timeline(screen_name=username, count=count, max_id=oldest_id)
    return [tweet._json for tweet in tweets]


def main():
    # Authentication
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    # Initialize API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    all_tweets = []
    new_tweets = get_tweets(api, USERNAME)
    
    all_tweets += new_tweets
    oldest_id = new_tweets[-1]["id"] - 1
    
    # Retrieve all tweets (up to the most recent ~3200)
    while len(new_tweets) > 0:
        new_tweets = get_tweets(api, USERNAME, oldest_id=oldest_id)
        all_tweets += new_tweets
        oldest_id = all_tweets[-1]["id"] - 1
        print(f"{len(all_tweets)} tweets retrieved")
    
    with open(f"data/UserTimeline_{USERNAME}.json", 'w') as f:
        json.dump(all_tweets, f)
    
    # # You can load the json into a pandas dataframe with:
    # with open("data.json", 'r') as f:
    #     data = json.load(f)
    #     df = pd.DataFrame(data)

if __name__ == "__main__":
    main()