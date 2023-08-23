from flask import Flask, request, render_template, redirect, url_for, session
import urllib
from datetime import datetime
import requests as pyreq
import init
import db

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

def token_expired(user):
	return False

def refresh_token(user):
	return user

def get_activities(user, page, activities_per_page):
	if token_expired(user):
		user = refresh_token(user)
	access_token = user['token']
	strava_req = pyreq.get(
		'https://www.strava.com/api/v3/athlete/activities',
		headers = {
			'accept': 'application/json',
			'authorization': 'Bearer '+access_token
		},
		params = {
			'per-page': ''+activities_per_page,
			'page': ''+page
		}
	)
	return strava_req

def get_activity(user, activity_id):
	if token_expired(user):
		user = refresh_token(user)
	access_token = user['token']
	strava_req = pyreq.get(
		'https://www.strava.com/api/v3/activities/{}'.format(activity_id),
		headers = {
			'accept': 'application/json',
			'authorization': 'Bearer '+access_token
		}
	)
	return strava_req

@app.template_filter('strftime')
def _string_to_datetime(input, fmt=None):
	date = datetime.strptime(input, "%Y-%m-%dT%H:%M:%SZ")
	if not fmt:
		fmt = "%Y-%m-%d"
	return date.strftime(fmt)

@app.route("/")
def splash():
	testpost = {'heading': "testing title", 'body': 'testing body'}
	return render_template('splash.html', post=testpost)

@app.route("/loggedin", methods=['GET'])
def loggedin():
	activities = []
	name = 'No Name!'
	if request.method == "GET":
		code = request.args.get('code')
		if not code:
			return redirect(url_for("splash"))
		strava_response = exchange_token(code).json()
		name = strava_response['athlete']['firstname']
		strava_user_id = strava_response['athlete']['id']
		access_token = strava_response['access_token']
		refresh_token = strava_response['refresh_token']
		expires_at = strava_response['expires_at']
		session['id'] = strava_user_id
		session['activities_per_page'] = 15
		# store user info in db
		db.store_user(name, strava_user_id, access_token, refresh_token, expires_at)
		return redirect(url_for("activities", page=1))

@app.route("/activities/<int:page>")
def activities(page):
	if not session['id']:
		print("no session id!")
		return redirect(url_for('splash'))
	# get name and access token from db
	user = db.fetch_user(session['id'])
	if not user:
		print("no user for user_id ", session['id'])
		return redirect(url_for('splash'))
	activities = get_activities(user, page, session['activities_per_page']).json()
	return render_template("loggedin.html", page=page, name=user['name'], activities=activities)

@app.route("/_show_activity/<int:activity_id>", methods=['POST'])
def show_activity(activity_id):
	user = db.fetch_user(session['id'])
	activity = get_activity(user, activity_id)
	return activity.json()

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
