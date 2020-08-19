import requests
import json
import os
import re
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "<h1> Deployed to Heroku</h1>"

@app.route('/webhook', methods=['POST'])
def respond():
	raw_payload = request.get_json()
	raw_event_type = raw_payload["event_type"]
	event_type = re.findall('[A-Z][^A-Z]*', raw_event_type)[1]
	resource_name = raw_payload["resource_name"]
	created_at = raw_payload["created_at"]
	resource = raw_payload["resource"]
	payload = "At "+created_at+", the "+resource+" named "+resource_name+" was "+event_type
	print(payload)
	slack_payload = json.dumps({'text': '{}'.format(payload)})
	slack_url = os.environ.get('SLACK_WEBHOOKS_URL')

	requests.post(slack_url, data=slack_payload)

	return '', 200


if __name__ == '__main__':
    app.run()
