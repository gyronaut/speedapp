import os
from flask import Flask, request
import requests as pyreq

def subscribe_to_webhook(app):
    strava_response = pyreq.post(
        "https://www.strava.com/api/v3/push_subscriptions",
        data={
            'client_id': app.config['CLIENT_ID'],
            'client_secret': app.config['CLIENT_SECRET'],
            'callback_url': "http://www.gyronautilus.com/webhook",
            'verify_token': app.config['VERIFY_TOKEN']
        }
    )

def create_app():
    app = Flask(__name__)
    app.config.update(
        CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID'),
        CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET'),
        REDIRECT_URI = 'http://www.gyronautilus.com/speedapp/loggedin',
        VERIFY_TOKEN = "stravatokenshhh",
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        PER_PAGE = 15
    )

    secret_key = app.secret_key
    if not secret_key:
        raise ValueError("No Secret Key was set in the create_app() method!!")

    @app.route("/webhook",methods=['POST', 'GET'])
    def webhook():
        if request.method == 'POST':
            print("Recieved data from webhook: ", request.json)
            return "received webhook", 200
        if request.method == 'GET':
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            if(mode and token):
                if(mode == 'subscribe' and token == app.config['VERIFY_TOKEN']):
                    response = {"hub.challenge": challenge}
                    return response, 200
                else:
                    return 'Authorization denied! token mismatch', 403

    subscribe_to_webhook(app)
    return app
