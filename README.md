# twitter-scraping

Twitter news searcher in Python.

Using tweepy to connect with Twitter api. Need to get consumer_key, consumer_secret, access_token, access_token_secret from Twitter account.

Words.txt is text dictionary with searching words. 

# Simple algorithm:

1. Connection with Twitter by tweepy.
2. Choose the date (since, until time), language, mode.
3. Get all the tweets with urls. 
4. Get all the tweets from reliable source (the user has a website and its name hasn't got some weird chars).
5. Search for tweets connected to our dictionary words.
6. Save the date, username, text and hashtags of tweets in .xlsx file.


