import os
from flask import Flask, request, render_template, redirect, jsonify
import urllib
import requests as pyreq
import init

app = init.create_app()

def exchange_token(code):
	strava_req = pyreq.post(
		'https://www.strava.com/oauth/token',
		data={
				'client_id': app.config['CLIENT_ID'],
            	'client_secret': app.config['CLIENT_SECRET'],
            	'code': code,
            	'grant_type': 'authorization_code'
        	}
	)
	return strava_req

def get_activities(access_token):
	strava_req = pyreq.get(
		'https://www.strava.com/api/v3/athlete/activities?per_page=30',
		headers={
			'accept': 'application/json',
			'authorization': 'Bearer '+access_token
		}
	)
	return strava_req

@app.route("/")
def test():
	testpost = {'heading': "testing title", 'body': 'testing body'}
	return render_template('splash.html', post=testpost)

@app.route("/loggedin", methods=['GET'])
def init():
	activities = [{'date': '2023-01-01', 'name': 'test', 'type':'ride test'}]
	name = 'No Name!'
	if request.method == "GET":
		code = request.args.get('code')
		if not code:
			return "Missing code parameter!", 400		
		strava_response = exchange_token(code).json()
		name = strava_response['athlete']['firstname']
		userid = strava_response['athlete']['id']
		access_token = strava_response['access_token']
		activities = get_activities(access_token)
	return render_template('loggedin.html',name=name,activities=activities)

@app.route("/auth", methods=['GET'])
def authorize():
	url = 'https://www.strava.com/oauth/authorize'
	params = {
		'client_id': app.config['CLIENT_ID'],
		'redirect_uri': app.config['REDIRECT_URI'],
		'response_type': 'code',
		'scope': 'activity:read_all'
		}
	return redirect('{}?{}'.format(url, urllib.urlencode(params)))

if __name__ == "__main__":
	app.run()
