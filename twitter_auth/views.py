# -*- coding: utf-8 -*-
import tweepy
import uuid , json
from django.http import *
from django import template
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from models import *
from utils import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis import geos
from django.contrib.gis.measure import Distance, D
from django.contrib.gis.geos import GEOSGeometry, fromstr


	

def main(request):
	"""
	main view of app, either login page or info page
	"""
	# if we haven't authorised yet, direct to login page
	if check_key(request):
		return HttpResponseRedirect(reverse('info'))
	else:
		return render_to_response('twitter_auth/login.html')

def unauth(request):
	"""
	logout and remove all session data
	"""
	if check_key(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main'))

def info(request):
	if check_key(request):
		api = get_api(request)
		user = api.me()
		userid = user.id
		request.session['userid'] = userid
		jsonothers=user.profile_image_url
		if user.default_profile_image:
			return HttpResponseRedirect('http://google.com/')
		try:
			acc=account.objects.get(twitterid=userid)
		except account.DoesNotExist:
			smaluri = user.profile_image_url
			spliturl = smaluri.split("_normal")
			orginalurl = spliturl[0]+spliturl[1]
			registeracc=account(twitterid=userid, username = user.screen_name, name = user.name, followers = user.followers_count ,language= "en", bio = user.description , image = orginalurl)
			registeracc.save()
			return HttpResponseRedirect('http://nearano.com/location/')
		
		loggeraccount = account.objects.get(twitterid=userid)
		if(loggeraccount.location):
			loggeraccount.status = "online"
			loggeraccount.save()
			current_point = geos.fromstr(loggeraccount.location)
			shops = account.gis.filter(status="online", location__distance_lt =(current_point, D(km=10000)))
			shops = shops.distance(current_point).order_by('distance')[1:50]
			nearbys = []
			for near in shops:
				x = round(near.distance.km, 2)
				nearbys.append([near.username , x, near.image])
			
			offline = account.gis.filter(status="offline", location__distance_lt =(current_point, D(km=10000)))
			offline = offline.distance(current_point).order_by('distance')[1:6]
			offlineusers = []
			for off in offline:
				x = round(off.distance.km, 2)
				offlineusers.append([off.username , x, off.image])
			
			
			
			return render_to_response('twitter_auth/info.html', locals())
		else:
			return HttpResponseRedirect('http://nearano.com/location/')
	else:
		return HttpResponseRedirect(reverse('main'))	
	
	
	
	
	
	
	if check_key(request):                                                    
		api = get_api(request)
		user = api.me()
		return render_to_response('twitter_auth/info.html', locals())
	else:
		return HttpResponseRedirect(reverse('main'))

def auth(request):
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret) 
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.set_request_token(token[0], token[1])
    # get the access token and store
    try:
    	oauth.get_access_token(verifier)
    except tweepy.TweepError:
    	print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key
    request.session['access_secret_tw'] = oauth.access_token.secret
    response = HttpResponseRedirect(reverse('info'))
    return response

def check_key(request):
	"""
	Check to see if we already have an access_key stored, if we do then we have already gone through 
	OAuth. If not then we haven't and we probably need to.
	"""
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True



def location(request):
	try:
		userid = request.session['userid']
	except KeyError:
		return HttpResponseRedirect('http://nearano.com/logout/')
	return render_to_response('twitter_auth/take_location.html', locals())



@csrf_exempt
def location_updater(request):
	if request.method == 'POST':
		userid = request.session['userid']
		longitude = request.POST.get('lng').encode('utf-8')
		latitude =  request.POST.get('lat').encode('utf-8')
		current_point = geos.fromstr("POINT(%s %s)" % (longitude,latitude))
		print current_point
		pnt = GEOSGeometry(current_point)
		loggeraccount = account.objects.get(twitterid=userid)
		loggeraccount.location = pnt
		loggeraccount.save()
		return HttpResponse('welldone')
	else:
		return HttpResponse('eroor')
		
		
def userprofile(request, username):
    try:
        user = account.objects.get(username=username)
    except account.DoesNotExist:
        return HttpResponse('Cant find any user')

    image = user.image
    bio = user.bio
    uname = username
    followers = user.followers
    chatcount = user.speakcounter
    regdate = user.regdate
    ustatus = user.status
    try:
        whoisme = request.session['userid']
    except KeyError:
        whoisme = "null"
        return render_to_response('twitter_auth/profile.html', locals())
    return render_to_response('twitter_auth/profile.html', locals())


def locationshuffle(request, username):
	try:
		user = account.objects.get(username=username)
	except account.DoesNotExist:
		return HttpResponse('Error')
	current_point = geos.fromstr(user.location)
	shops = account.gis.filter(location__distance_lt =(current_point, D(km=10000)))
	shops = shops.distance(current_point).order_by('distance')[1:50]
	
	nearbys = []
	for dis in shops:
		x = round(dis.distance.km, 2)
		nearbys.append([dis.username , x, dis.location[0], dis.location[1] ])
	#print usercoord # welldone
	#print nearbys
	api = {"nearbys": nearbys}
	jls = json.dumps(api)
	return HttpResponse('%s'% jls)  






