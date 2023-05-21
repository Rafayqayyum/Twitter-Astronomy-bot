from requests_oauthlib import OAuth1Session
import os

API_KEY=os.environ.get('API_KEY')
API_KEY_SECRET=os.environ.get('API_KEY_SECRET')

# authorize the app and get the resource owner key and secret
def authorize_app():
    oauth = OAuth1Session(client_key=API_KEY, client_secret=API_KEY_SECRET)
    fetch_response=oauth.fetch_request_token('https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write')
    resource_owner_key=fetch_response.get('oauth_token')
    resource_owner_secret=fetch_response.get('oauth_token_secret')
    base_authorization_url='https://api.twitter.com/oauth/authorize'
    authorization_url=oauth.authorization_url(base_authorization_url)
    print(authorization_url)
    verifier=input('Enter the verifier:')
    oauth=OAuth1Session(client_key=API_KEY,client_secret=API_KEY_SECRET,resource_owner_key=resource_owner_key,resource_owner_secret=resource_owner_secret,verifier=verifier)
    oauth_tokens=oauth.fetch_access_token('https://api.twitter.com/oauth/access_token')
    resource_owner_key=oauth_tokens.get('oauth_token')
    resource_owner_secret=oauth_tokens.get('oauth_token_secret')
    print(resource_owner_key)
    print(resource_owner_secret)

if __name__=='__main__':
    authorize_app()