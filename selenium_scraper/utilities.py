from selenium.webdriver.common.by import By


def get_tweet_text(tweet):
    tweet_text = tweet.find_element(By.CSS_SELECTOR, "[data-testid=tweetText]")
    return tweet_text.get_attribute("textContent")

def get_tweet_time(tweet):
    tweet_time = tweet.find_element(By.TAG_NAME, "time")
    return tweet_time.get_attribute("datetime")

def get_tweet_replies(tweet):
    tweet_replies = tweet.find_element(By.CSS_SELECTOR, "[data-testid=reply]")
    return int(tweet_replies.get_attribute("aria-label").split(" ")[0])

def get_tweet_retweets(tweet):
    tweet_retweets = tweet.find_element(By.CSS_SELECTOR, "[data-testid=retweet]")
    return int(tweet_retweets.get_attribute("aria-label").split(" ")[0])

def get_tweet_likes(tweet):
    tweet_likes = tweet.find_element(By.CSS_SELECTOR, "[data-testid=like]")
    return int(tweet_likes.get_attribute("aria-label").split(" ")[0])

def get_tweet_views(tweet, num):
    tweet_views = tweet.find_elements(By.XPATH, "//a[contains(@aria-label, 'View Tweet analytics')]")[num]
    return int(tweet_views.get_attribute("aria-label").split(" ")[0])

def get_tweet_link(tweet, num):
    tweet_link = tweet.find_elements(By.XPATH, "//a[contains(@aria-label, 'View Tweet analytics')]")[num]
    return tweet_link.get_attribute("href")[:-10]