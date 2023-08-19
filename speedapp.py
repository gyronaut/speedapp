import os
from flask import Flask, request, render_template, redirect 
import urllib

app = Flask(__name__)


CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = 'http://gyronautilus.com/speedapp/strava_redirect'

@app.route("/")
def test():
    	testpost = {'heading': "testing title", 'body': 'testing body'}
	return render_template('index.html', post=testpost)

@app.route("/strava_redirect")
def init():
	activities = {}
	return render_template('loggedin.html',activities=activities)

@app.route("/strava_auth", methods=['GET'])
def authorize():
	url = 'https://www.strava.com/oauth/authorize'
	params = {
		'client_id': CLIENT_ID,
		'redirect_uri': REDIRECT_URI,
		'response_type': 'code',
		'scope': 'activity:read_all'
		}
	return redirect('{}?{}'.format(url, urlib.urlencode(params)))

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
				return '', 403

if __name__ == "__main__":
	app.run()
