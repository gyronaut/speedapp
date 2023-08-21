import os
from flask import Flask, request, render_template, redirect, jsonify, url_for
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
def splash():
	testpost = {'heading': "testing title", 'body': 'testing body'}
	return render_template('splash.html', post=testpost)

@app.route("/loggedin/<int:user_id>")
@app.route("/loggedin", methods=['GET'])
def loggedin(user_id = None):
	activities = []
	name = 'No Name!'
	if not user_id:
		if request.method == "GET":
			code = request.args.get('code')
			if not code:
				return "Missing code parameter!", 400		
			strava_response = exchange_token(code).json()
			name = strava_response['athlete']['firstname']
			strava_user_id = strava_response['athlete']['id']
			access_token = strava_response['access_token']
			# store name, id, and user token in db
			return redirect(url_for("loggedin", user_id = strava_user_id))
		return redirect(url_for("splash"))
	# get name and access token from db
	name = "test"
	access_token = ""
	activities = get_activities(access_token).json()
	return render_template("loggedin.html", name=name, activities=activities)



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
