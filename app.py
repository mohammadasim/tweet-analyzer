from user import User
import constants
import oauth2
import urllib.parse as urlparse
import json


consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def create_authorized_user(email, first_name, last_name):
    client = oauth2.Client(consumer)
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print('An error has occured')
    request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    print('Please click the following link to get a pin')
    print('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token']))
    verified_pin  = input('Please enter the pin received from Tweeter:  ')
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(verified_pin)
    client = oauth2.Client(consumer, token)
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'])
    user.save_to_db()
    return user


def create_twitter_query(email, twitter_url, request_verb):
    user = User.find_by_email(email)
    authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
    authorized_client = oauth2.Client(consumer, authorized_token)
    response, content = authorized_client.request(twitter_url, request_verb)
    if response.status != 200:
        print('An error has happened. Received this status code {}'.format(response.status))
    result = json.loads(content.decode('utf-8'))
    return result


result = create_twitter_query('asim.kdr@gmail.com', 'https://api.twitter.com/1.1/search/tweets.json?q=brexit', 'GET')
for element in result['statuses']:
    print(element['text'])
