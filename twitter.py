# import required packages
from requests_oauthlib import OAuth1Session
from nasa_apod import get_random_picture_of_the_day
import os
import time
CHARACTER_LIMIT=280
MEDIA_URL='https://upload.twitter.com/1.1/media/upload.json'
TWEET_URL="https://api.twitter.com/2/tweets"
DELETE_TWEET_URL="https://api.twitter.com/2/tweets/:id"
API_KEY=os.environ.get('API_KEY')
API_KEY_SECRET=os.environ.get('API_KEY_SECRET')
RESOURCE_OWNER_KEY=os.environ.get('RESOURCE_OWNER_KEY')
RESOURCE_OWNER_SECRET=os.environ.get('RESOURCE_OWNER_SECRET')

def connect_to_oauth():
    try:
        oauth=OAuth1Session(client_key=API_KEY,client_secret=API_KEY_SECRET,resource_owner_key=RESOURCE_OWNER_KEY,resource_owner_secret=RESOURCE_OWNER_SECRET)  
        return oauth
    except Exception as e:
        print('Problem connecting to the twitter API'+'\n'+str(e))
        exit()

# function to divide a string into chunks of a character limit
# divide on the basis of words
def divide_string_into_chunks(title,explanation,hdurl,date,character_limit=CHARACTER_LIMIT): 
    # extract the date from the date object
    # DD-MM-YYYY
    date=date.strftime('%d-%m-%Y')
    # creating chunk list to store the chunks
    chunks=[]
    # append the title to the chunks
    chunks.append(title+'\n')
    # append the date to the chunks
    chunks[0]+= "Date: "+date+'\n'
    i=0
    for word in explanation.split():
        if len(chunks[i]+word+' ') < character_limit:
            chunks[i]+=word+' '
        else:
            chunks.append(word+' ')
            i+=1
    if len(chunks[i]+f"\n HD-URL: {hdurl}") < character_limit:
        chunks[i]+=f"\n HD-URL: {hdurl}"
    else:
        chunks.append(f"\n HD-URL: {hdurl}")
    return chunks
    
    

# function to post a tweet with a picture of the day
def post_tweet_with_picture_of_the_day():
    # get a random picture of the day
    print('Getting a random picture of the day...')
    try:
        title, explanation, path, hdurl, date = get_random_picture_of_the_day()
    except Exception as e:
        print("Failed to get a random picture")
        print(str(e))
        # return error code and message
        return  {'statusCode': 500,'body': 'Failed to get a random picture'}
    # divide the explanation into chunks of a character limit
    print ('Dividing the explanation into chunks of a character limit...')
    chunks=divide_string_into_chunks(title,explanation,hdurl,date)
    # connect to the twitter API
    try:
        print('Connecting to the twitter API...')
        oauth = connect_to_oauth()
    except Exception as e:
        print("Failed to connect to the twitter API")
        print(str(e))
        return  {'statusCode': 500,'body': 'Failed to connect to the twitter API'}
    
    # upload the picture of the day
    print('Uploading the picture of the day...')
    response=''
    try:
        response = oauth.post(url=MEDIA_URL, files={"media": open(path, 'rb')})
    except Exception as e:
        print("Failed to upload the picture")
        print(str(e))
        return  {'statusCode': 500,'body': 'Failed to upload the picture'}
    # create the first tweet with the picture of the day
    print('Creating the first tweet with the picture of the day...')
    tweet_responses=[]
    base_tweet=''
    try:
        base_tweet = oauth.post(url=TWEET_URL, json={"text": chunks[0],"media":{"media_ids": [response.json().get('media_id_string')]}})
        tweet_responses.append(base_tweet)
    except Exception as e:
        print("Failed to create the first tweet")
        print(str(e))
        return  {'statusCode': 500,'body': 'Failed to create the first tweet'}
    try:
        # add the remaining chunks to the tweet
        for i,chunk in enumerate(chunks[1:]):
            # sleep for 2 seconds
            time.sleep(2)
            # create the tweet
            print ('Creating the tweet...'+' '+str(i+1))
            base_tweet = oauth.post(url=TWEET_URL, json={"text": chunk,"reply":{"in_reply_to_tweet_id": tweet_responses[i].json().get('data').get('id')}})
            # if tweet wasn't created successfully, delete the ones that were created
            if base_tweet.status_code!=201 and base_tweet.status_code!=200:
                    raise Exception(base_tweet.json().get('errors')[0].get('message'))
            tweet_responses.append(base_tweet)
            
        # return success code and message
        return  {'statusCode': 200,'body': 'Successfully created the sub tweets'}
            
    except Exception as e:
        # print the exception message
        print("Failed to create the sub tweets")
        print(str(e))
        # if all tweets weren't created successfully, delete the ones that were created
        if not all(tweet.status_code==201 or tweet.status_code==200 for tweet in tweet_responses):
            print('Deleting all tweets...')
            for tweet in tweet_responses:
                if tweet!= None:
                    print(tweet.status_code)
                    if tweet.status_code==201 or tweet.status_code==200:
                        oauth.delete(url=DELETE_TWEET_URL.replace(':id',tweet.json().get('data').get('id')))
        return  {'statusCode': 500,'body': 'Failed to create the sub tweets, deleted all tweets'}

if __name__ == '__main__':
    # post a tweet with a picture of the day
    response = post_tweet_with_picture_of_the_day()
    
