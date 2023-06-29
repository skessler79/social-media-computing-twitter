from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver import ActionChains

import json
import time
import warnings

from utilities import get_tweet_text, get_tweet_time, get_tweet_replies, get_tweet_retweets, get_tweet_likes, get_tweet_views, get_tweet_link

# USERNAME = "TheBabylonBee"
# USERNAME = "HardDriveMag"
# USERNAME = "TheOnion"
USERNAME = "Reductress"

all_tweets = {}

# Webdriver options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
chromedriver = "./chromedriver"    # Place the path to your chromedriver

warnings.filterwarnings("ignore", category=DeprecationWarning) 

# Create webdriver
driver = webdriver.Chrome(options=options, executable_path=chromedriver)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get(f"https://twitter.com/{USERNAME}")

# TODO : Close notification popup
while True:
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-testid=app-bar-close]").click()
        break
    except:
        pass

# Main loop
for i in range(200):
    if i % 20 == 0:
        print(i)
        
    # Get loaded tweets
    tweets = driver.find_elements(By.TAG_NAME, "article")
    for num, tweet in enumerate(tweets):
        
        try:
            # Skip retweets not by the user
            tweet_user = tweet.find_element(By.CSS_SELECTOR, "[data-testid=User-Name]")
            tweet_username = tweet_user.text.split('\n')[1][1:]
            if tweet_username != USERNAME:
                continue
            
            # Get tweet text
            tweet_text = get_tweet_text(tweet)
            
            # Get tweet time
            tweet_time = get_tweet_time(tweet)

            # Get tweet reply count
            tweet_replies = get_tweet_replies(tweet)
            
            # Get tweet retweet count
            tweet_retweets = get_tweet_retweets(tweet)
            
            # Get tweet like count
            tweet_likes = get_tweet_likes(tweet)
            
            # Get tweet view count
            tweet_views = get_tweet_views(tweet, num)
            
            # Get tweet link
            tweet_link = get_tweet_link(tweet, num)

            # Insert into dictionary
            if not tweet_link in all_tweets.keys():
                tweet_info = {"text" : tweet_text,
                            "time" : tweet_time,
                            "replies" : tweet_replies,
                            "retweets" : tweet_retweets,
                            "likes" : tweet_likes,
                            "views" : tweet_views
                            }
                
                all_tweets[tweet_link] = tweet_info
        except Exception as e:
            pass
        
    # Scroll to bottom of loaded tweets
    bottom = -1
    while True:
        try:
            ActionChains(driver).scroll_to_element(tweets[bottom]).perform()
            break
        except:
            bottom -= 1
    
    time.sleep(1.5)

with open(f"output_selenium_{USERNAME}.json", 'w') as file:
    json.dump(all_tweets, file)
    
print("done")
    