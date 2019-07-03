import constants
import oauth2
import urllib.parse as urlparse
import json

# Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# Use the client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

if response.status != 200:
    print('An error occurred getting the request token from Twitter')


# the content received is in the form of a query string, The parse_qsl change it into a list of tuples, dict method change it into a dictionary
# The decode method changes it from bytes to strings

request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

# Steps for user
# customer visits our website www.ourwebsite.com and click log in with twitter button
# They are redirected to twitter and they sign in or authorize
# Twitter sends them back to our website www.ourwebsite.com/auth
# We get that auth code + request token and send them to twitter and twitter sends us the access token

# Ask the user to authorize our app and give us the pin code
print('To to the following site in your browser:')
print('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_pin = input('What is the PIN? ')

# We create a token object that consists of request_token parameters and the pin code (verifier) given by twitter
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_pin)

# Create a client with our consumer (our app) and the newly created (and verified) token
client = oauth2.Client(consumer, token)

# Ask Twitter for an access token, and Twitter know it should give it to us because we have verified the request token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
print(access_token)

# Create an 'authorized_token' Token object and use that to perform API Calls on behalf of the user

authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

# Make Twitter API calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
if response.status != 200:
    print('An error happened')

tweets = json.loads(content.decode('utf-8'))

for value in tweets['statuses']:
    print(value['text'])