from flask import Flask, request, render_template, redirect, url_for, session
import urllib
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

def get_activities(user, page):
	if token_expired(user):
		user = refresh_token(user)
	access_token = user['access_token']
	strava_req = pyreq.get(
		'https://www.strava.com/api/v3/athlete/activities',
		headers = {
			'accept': 'application/json',
			'authorization': 'Bearer '+access_token
		},
		params = {
			'per-page':30,
			'page':page
		}
	)
	return strava_req

def get_activity(user, activity_id):
	if token_expired(user):
		user = refresh_token(user)
	access_token = user['access_token']
	strava_req = pyreq.get(
		'https://www.strava.com/api/v3/activities/{}'.format(activity_id),
		headers = {
			'accept': 'application/json',
			'authorization': 'Bearer '+access_token
		}
	)
	return strava_req

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
		session['activity_page'] = 1
		# store user info in db
		db.store_user(name, strava_user_id, access_token, refresh_token, expires_at)
		return redirect(url_for("activities", page=1))

@app.route("/activities/<int:page>")
def activities(page):
	if not session['id']:
		return redirect('/splash')
	# get name and access token from db
	name = "test"
	user = db.fetch_user(session['id'])
	if not user:
		return redirect('/splash')
	activities = get_activities(user, page).json()
	return render_template("loggedin.html", name=name, activities=activities)

@app.route("activities/<int:page>/<int:activity_id>", methods=['POST'])
def show_activity(page, activity_id):
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
