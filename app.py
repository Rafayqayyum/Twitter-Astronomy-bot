# create a flask route to execute the function
from twitter import post_tweet_with_picture_of_the_day
import os
from flask import Flask
from flask import request, make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    secret_key=request.headers.get("Secret-Key")
    if secret_key != os.environ.get('SECRET_KEY'):
        return make_response('Invalid Secret Key', 401)
    else:
        return make_response('Hello, World!', 200)
    
@app.route('/post_tweet_with_picture_of_the_day')
def post_tweet_with_picture_of_the_day_route():
    # get the request header
    secret_key=request.headers.get("Secret-Key")
    # get the secret key from the request header
    secret_key = request.headers.get('SECRET_KEY')
    if secret_key != os.environ.get('SECRET_KEY'):
        # return status 401 if the secret key is invalid
        return make_response('Invalid Secret Key', 401)
    else:
        # execute the function
        post_tweet_with_picture_of_the_day()
        # return status 200 
        return make_response('Tweeted Successfully', 200)

if __name__ == '__main__':
    app.run()
