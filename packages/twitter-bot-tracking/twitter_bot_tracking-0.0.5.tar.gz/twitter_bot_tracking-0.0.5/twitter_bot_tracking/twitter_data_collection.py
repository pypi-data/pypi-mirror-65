import json, time, datetime, tweepy, math, functools
from .twitter_api_preparation import TwitterAPIsList, TwitterAPI
from abc import ABCMeta, abstractmethod
from langdetect import detect


class APIsCursor:
    """ This class is responsible for changing the API when it reaches to the maximum
        limit
    """
    def __init__(self, waiting_period=0.5, maximum_period=900):
        
        self.apis = TwitterAPIsList()
        self.number_of_trials = 0
        self.number_of_apis = self.apis.number_of_apis
        self.waiting_period = waiting_period
        self.cur_waiting_period = waiting_period
        self.maximum_period = maximum_period
        self.current_api = -1
        
    def update(self, required_function=None):
        """ Check what is the next available API """
        
        if self.number_of_trials == self.number_of_apis:
            # All the apis exceed the rate limit
    
            # Reset number of trials
            self.number_of_trials = 0
            
            # Waiting
            self.cur_waiting_period *= 2
            print(f'Waiting for : {self.cur_waiting_period}')
            time.sleep(self.cur_waiting_period)
            
            if self.cur_waiting_period > self.maximum_period:
                self.cur_waiting_period = self.waiting_period
                
        else:
            self.number_of_trials += 1
            
            # Use the next api
            self.current_api = (self.current_api + 1) % self.number_of_apis
            print(f'Using the api number {self.current_api} for the request')
        
        api = self.apis[self.current_api]
        
        if required_function:
            # Return the required function from the active API
            return getattr(api, required_function)
        return api


class TweetsCollector(metaclass=ABCMeta):
    """ This is the parent class for any class to collect tweets """
    def __init__(self, search_params, collection_function):
        self.search_params = search_params
        
        
        self.tweets = []   # Empty list to keep the collected tweets
        self.collection_function = collection_function   # The required function to collect data
        self.api_cursor = APIsCursor()  # Cursor to change the API what hitting the limit
        
        self.tweets_cursor = None
        self.update_tweets_cursor()
        
        self.collection_done = False  # Flag to exit once collection is done
    
    def update_tweets_cursor(self):
        """ Get another api function cursor when hitting the limit """
        # Update max_id to collect tweets that are before the tweets 
        # that already is collected
        common_search_parms = {
            'max_id': None if len(self.tweets) == 0 else self.tweets[-1].id
        }

        collector = self.api_cursor.update(self.collection_function)
        self.tweets_cursor = tweepy.Cursor(
            collector, **{**common_search_parms, **self.search_params}).pages()
    

    def filter_out_repeated_tweets(self):
        """ This function will filter out any possible repeated tweet """
        print('Filtering ....')
        tweets_dict = {tw.id_str: tw for tw in self.tweets}

        if len(tweets_dict) != len(self.tweets):
            print('Number of repeated tweets is : ', len(self.tweets)- len(tweets_dict) )
            
            # Take the unique tweets only
            self.tweets = list(tweets_dict.values())
    
    @abstractmethod
    def collect(self):
        pass


class UserTimelineTweetsCollector(TweetsCollector):
    """ This class is to collect tweets according to a user id """
    
    def __init__(self, search_params):
        super().__init__(search_params, 'user_timeline') 
    
    def collect(self, number_of_tweets=math.inf):
        """ This function collects tweets and stops when the number of tweets
            reaches number_of_tweets
        """
        
        while not self.collection_done:
            try:
                page = next(self.tweets_cursor)
                
                for tw in page:
                    self.tweets.append(tw)
                    
                    if len(self.tweets) == number_of_tweets:
                        raise StopIteration
            
            except tweepy.TweepError:
                if TwitterAPI.is_rate_limit_error(e):
                    # Hitting the rate limit. Therefore, change the API
                    self.update_tweets_cursor()
                else:
                    # Unknown: it should be fixed once happening
                    raise e
            
            except StopIteration:
                # No More Tweets
                self.collection_done = True
                break


class QueryTweetsCollector(TweetsCollector):
    """ This class is to collect tweets according to a keyword """
    
    def __init__(self, search_params):
        super().__init__(search_params, 'search') 
    
    
    def collect(self, filter_on_english, number_of_tweets=math.inf):
        """ This function collects tweets and stops when the number of unique account
            reaches number_of_accounts
        """
        tweets_accounts = set()
        
        while not self.collection_done:
            try:
                page = next(self.tweets_cursor)
                
                for tw in page:
                    if filter_on_english:
                        try:
                            if detect(tw._json['full_text']) == 'en':
                                self.tweets.append(tw)

                        except:
                            pass
                    
                    if len(self.tweets) == number_of_tweets:
                        raise StopIteration
            
            except tweepy.TweepError as e:
                if TwitterAPI.is_rate_limit_error(e):
                    # Hitting the rate limit. Therefore, change the API
                    self.update_tweets_cursor()
                else:
                    # Unknown: it should be fixed once happening
                    raise e
            
            except StopIteration:
                # No More Tweets
                self.collection_done = True
                break


class FavoritedTweetsCollector(TweetsCollector):
    """ This class is to collect the favourited tweets by a user """
    
    def __init__(self, search_params):
        super().__init__(search_params, 'favorites') 
    
    def collect(self, number_of_tweets=math.inf):
        """ This function collects tweets and stops when the number of tweets
            reaches number_of_tweets
        """
        
        while not self.collection_done:
            try:
                page = next(self.tweets_cursor)
                
                for tw in page:
                    self.tweets.append(tw)
                    
                    if len(self.tweets) == number_of_tweets:
                        raise StopIteration
            
            except tweepy.TweepError as e:
                
                if TwitterAPI.is_rate_limit_error(e):
                    # Hitting the rate limit. Therefore, change the API
                    self.update_tweets_cursor()
                else:
                    # Unknown: it should be fixed once happening
                    raise e
                
            except StopIteration:
                # No More Tweets
                self.collection_done = True
                break


class DataCollector:
    """ This class is to collect any type of data from twitter except tweets(Refer to tweets
        collector) 
    """
    def __init__(self, required_function):
        self.api_cursor = APIsCursor()  # Cursor to change the API what hitting the limit
        self.required_function = required_function  # The function to be used to get the data
        self.function = None
        self.update_api_function()
    
    def update_api_function(self):
        self.function = self.api_cursor.update(self.required_function)
    
    def get(self, *args, **kwargs):
        while True:
            try:
                data = self.function(*args, **kwargs)
                break
            except tweepy.TweepError as e:
                if TwitterAPI.is_rate_limit_error(e):
                    self.update_api_function()
                else:
                    raise e
        return data
    
    @staticmethod
    def get_user_collector():
        return DataCollector('get_user')
    
    @staticmethod
    def get_status_collector():
        return DataCollector('get_status')
    
    @staticmethod
    def show_friendship_collector():
        return DataCollector('show_friendship')
    
    @staticmethod
    def trends_available_collector():
        return DataCollector('trends_available')
    
    @staticmethod
    def trends_place_collector():
        return DataCollector('trends_place')
