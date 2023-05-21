# this py file is the entry point for the lambda function
from twitter import post_tweet_with_picture_of_the_day
def lambda_function(event, context):
    res=post_tweet_with_picture_of_the_day()
    return res