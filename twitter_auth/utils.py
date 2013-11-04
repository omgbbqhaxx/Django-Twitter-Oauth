import tweepy

CONSUMER_KEY = 'Pimhpf45Po9Uy88lMs91FQ'
CONSUMER_SECRET = 'EYgXu1KEWQBANCzTz84Z56BuMBwRvEN5qcfdYZP2u0'

def get_api(request):
# set up and return a twitter api object
  oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  access_key = request.session['access_key_tw']
  access_secret = request.session['access_secret_tw']
  oauth.set_access_token(access_key, access_secret)
  api = tweepy.API(oauth)
  return api