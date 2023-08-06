import tweepy
import json
from abc import abstractmethod, ABCMeta


class DataAPIInterface(metaclass=ABCMeta):
    """ Interface class to all data source api """
    @abstractmethod
    def get_current_usage(self):
        pass
    

class TwitterAPI(tweepy.API, DataAPIInterface):
    """ This class is to get a signed in API
        Also it has some extra functionalities required to know the state of the API
    """
    def __init__(self, token, wait_on_rate_limit=False, 
                 timeout=10, retry_count=3):
        """ create a signed in twitter API
            Inputs:
            token: a dictionary of four keys consumer_key, consumer_secret, access_token, 
                   and access_token_secret
        """
        
        self.token = token
        
        auth = tweepy.OAuthHandler(self.token['consumer_key'],
                                   self.token['consumer_secret'])
        auth.set_access_token(self.token['access_token'],
                              self.token['access_token_secret'])
        super().__init__(auth, wait_on_rate_limit=wait_on_rate_limit,
                             timeout=timeout, retry_count=retry_count)
    
    def get_current_usage(self):
        """ Get the limit of and how much is used from each required API endpoint
            You can append to this dictionary what is important for you
        """
        rate_limit = self.rate_limit_status()
        

        return             {
                'rate_limit_status': rate_limit['resources']['application']['/application/rate_limit_status'],
                'show_friendship': rate_limit['resources']['friendships']['/friendships/show'],
                'get_user': rate_limit['resources']['users']['/users/show/:id'],
                'get_followers_list': rate_limit['resources']['followers']['/followers/list'],
                'get_followers_ids': rate_limit['resources']['followers']['/followers/ids'],
                'get_friends_list': rate_limit['resources']['friends']['/friends/list'],
                'get_friends_ids': rate_limit['resources']['friends']['/friends/ids'],
                'search_api': rate_limit['resources']['search'],
                'user_timeline': rate_limit['resources']['statuses']['/statuses/user_timeline'],
                'user_favourited_statuses': rate_limit['resources']['favorites']['/favorites/list'],
                'trends_available': rate_limit['resources']['trends']['/trends/available'],
                'trends_place': rate_limit['resources']['trends']['/trends/place']
            
            }
    
    @staticmethod
    def is_rate_limit_error(e):
        return '429' in e.reason or '88' in e.reason
    
    @staticmethod
    def resource_was_not_found(e):
        return '34' in e.reason


class TwitterAPIsList:
    """ This class manages the available twitter apis 
        It is a singleton class where the signing in happens only one time
    """
    _shared_state = {}   # This is required to make the class a singleton class

    def __new__(cls, *args, **kwargs):
        """ This is required to make the class a singleton class """
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj
    
    def __init__(self, tokens_file_path='twitter_tokens.json'):
        """ Create a list of all available twitter apis  """
        
        if len(TwitterAPIsList._shared_state):
            # No need to sign in again
            print('No need to sign in again')
            return
        
        # List of the available apis
        self.apis = []
        
        with open(tokens_file_path, 'r') as f:
            twitter_tokens = json.load(f)
            
            #for token in twitter_tokens:
            self.apis.append(TwitterAPI(twitter_tokens))
        
        self.number_of_apis = len(self.apis)
    
    def __getitem__(self, key):
        """ Get one of the available twitter API accounts """
        if key < 0 or key > self.number_of_apis-1:
            raise IndexError(f'The index should be in the range 0 to {self.number_of_apis-1}')
        return self.apis[key]
