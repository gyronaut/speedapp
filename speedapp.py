import os
from flask import Flask, request, render_template, redirect, jsonify
import urllib
import requests as pyreq

app = Flask(__name__)


CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = 'http://www.gyronautilus.com/speedapp/loggedin'

@app.route("/")
def test():
	testpost = {'heading': "testing title", 'body': 'testing body'}
	return render_template('splash.html', post=testpost)

@app.route("/loggedin", methods=['GET'])
def init():
	activities = {}
	name = 'No Name!'
	if request.method == "GET":
		code = request.args.get('code')
		if not code:
			return "Missing code parameter!", 400		
		strava_response = exchange_token(code).json()
		name = strava_response['athlete']['firstname']
		userid = strava_response['athlete']['id']
	return render_template('loggedin.html',name=name,activities=activities)

@app.route("/auth", methods=['GET'])
def authorize():
	url = 'https://www.strava.com/oauth/authorize'
	params = {
		'client_id': CLIENT_ID,
		'redirect_uri': REDIRECT_URI,
		'response_type': 'code',
		'scope': 'activity:read_all'
		}
	return redirect('{}?{}'.format(url, urllib.urlencode(params)))

def exchange_token(code):
	strava_req = pyreq.post(
		'https://www.strava.com/oauth/token',
		data={
			'client_id': CLIENT_ID,
            		'client_secret': CLIENT_SECRET,
            		'code': code,
            		'grant_type': 'authorization_code'
        	}
	)
	return strava_req

@app.route("/webhook",methods=['POST', 'GET'])
def webhook():
	if request.method == 'POST':
		print("Recieved data from webhook: ", request.json)
		return "received webhook", 200
	if request.method == 'GET':
		VERIFY_TOKEN = "stravatokenshhh"
		mode = request.args.get('hub.mode')
		token = request.args.get('hub.verify_token')
		challenge = request.args.get('hub.challenge')
		if(mode and token):
			if(mode == 'subscribe' and token == VERIFY_TOKEN):
				response = {"hub.challenge": challenge}
				return response, 200
			else:
				return 'Authorization denied! token mismatch', 403

if __name__ == "__main__":
	app.run()
