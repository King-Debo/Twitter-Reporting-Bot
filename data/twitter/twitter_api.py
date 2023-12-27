# Import the tweepy library
import tweepy

# Define the credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Define the query parameters
query = "#fakenews" # The hashtag to search for
count = 1000 # The number of tweets to retrieve
lang = "en" # The language of the tweets
result_type = "mixed" # The type of the tweets (mixed, recent, or popular)

# Search for tweets using the query parameters
tweets = api.search(q=query, count=count, lang=lang, result_type=result_type)

# Save the tweets in a CSV file
with open("twitter_data.csv", "w") as f:
    f.write("id,text,created_at,user,retweet_count,favorite_count\n") # Write the header
    for tweet in tweets:
        # Extract the relevant information from each tweet
        id = tweet.id # The tweet ID
        text = tweet.text.replace("\n", " ") # The tweet text
        created_at = tweet.created_at # The tweet creation date
        user = tweet.user.screen_name # The tweet user
        retweet_count = tweet.retweet_count # The tweet retweet count
        favorite_count = tweet.favorite_count # The tweet favorite count
        # Write the information in the CSV file
        f.write(f"{id},{text},{created_at},{user},{retweet_count},{favorite_count}\n")
