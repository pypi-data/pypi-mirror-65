#!/usr/bin/env python
# coding: utf-8

# In[3]:


import boto3
import os

# In[4]:


class DataAnalysis:

    
    @staticmethod
    def calculate_sentiment(data_df):
        
        # Add tweet sentiment column to dataframe
        data_df['sentiment'] = data_df.apply(
            lambda row: DataAnalysis.get_sentiment(row['text'], 
                                                   row['lang']), 
            axis=1)
        
        return data_df
    
    
    @staticmethod
    def get_sentiment(text, language):
        # Define comprehend object
        comprehend = boto3.client(service_name='comprehend',
                                  region_name=os.environ.get("region_name"))
        # Return undefined if language is not recognized by comprehend
        if language not in ['hi', 'de', 'zh-TW', 'ko', 'pt', 'en', 
                            'it', 'fr', 'zh', 'es', 'ar', 'ja']:

            return 'undefined'
        
        else:
            # Get detected sentiment as lower case string
            return comprehend.detect_sentiment(
                Text=text, LanguageCode=language)['Sentiment'].lower()
        
    @staticmethod
    def get_top_n(tweet_df, column, top_n):
        sorted_df = tweet_df.sort_values(column, ascending=False)[:top_n]
        return sorted_df


# In[ ]:




