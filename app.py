import requests
import json
import os
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "<h1> Deployed to Heroku</h1>"

@app.route('/webhook', methods=['POST'])
def respond():
	payload = request.get_json()
	slack_payload = json.dumps({'text': '{}'.format(payload)})
	slack_url = os.environ.get('SLACK_WEBHOOKS_URL')

	requests.post(slack_url, data=slack_payload)

	return '', 200


if __name__ == '__main__':
    app.run()
