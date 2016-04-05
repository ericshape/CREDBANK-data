# created by Ji Wang ericshape @ 4/5/16 11:48 AM

import tweepy
from api_key import API_Key

class Fetch_Tweet_By_ID():

    def __init__(self):
        # get api key from another configure file.
        api_key = API_Key()
        __CONSUMER_KEY = api_key.CONSUMER_KEY
        __CONSUMER_SECRET = api_key.CONSUMER_SECRET
        __OAUTH_TOKEN = api_key.OAUTH_TOKEN
        __OAUTH_TOKEN_SECRET = api_key.OAUTH_TOKEN_SECRET

        # init twitter api key in
        __auth = tweepy.OAuthHandler(__CONSUMER_KEY, __CONSUMER_SECRET)
        __auth.set_access_token(__OAUTH_TOKEN, __OAUTH_TOKEN_SECRET)
        self.api = tweepy.API(__auth,
                              wait_on_rate_limit_notify=True,
                              wait_on_rate_limit=True)

    def fetch_tweets(self, id_list):
        """fetch tweets via the list of tweet_ids
        :param id_list: a list of tweet_ids
        :return: None or tweet api json response.
        """
        if len(id_list) <= 100:
            return self.api.statuses_lookup(id_list)
        return None


if __name__ == '__main__':

    fetch_tweet_by_id = Fetch_Tweet_By_ID()

    # assign the tweet_id list for tweets retrieve.
    id_list = []

    tweet_json = fetch_tweet_by_id.fetch_tweets(id_list)

    if tweet_json:
        print(tweet_json)


