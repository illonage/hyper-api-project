import requests
import json
import os
import re
import tableauserverclient as TSC
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	TABLEAU_TOKEN = os.environ.get('TABLEAU_TOKEN')
	TABLEAU_SITE_NAME = os.environ.get('TABLEAU_SITE_NAME')
	TABLEAU_TOKEN_NAME = os.environ.get('TABLEAU_TOKEN_NAME')
	tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
                                                   personal_access_token=TABLEAU_TOKEN, site_id=TABLEAU_SITE_NAME)
	server = TSC.Server('https://10ax.online.tableau.com')

    # Set http options to disable verifying SSL
	server.add_http_options({'verify': False})
	server.use_server_version()

	with server.auth.sign_in_with_personal_access_token(tableau_auth):
			all_webhooks, pagination_item = server.webhooks.get()
			n = pagination_item.total_available
			html = "<h1>Welcome to your own Tableau Slackhooks</h1>"+"\n"
			html += "There are "+str(n)+" webhooks on your site:"+"\n"
			for webhook in all_webhooks:
				html += "<li>"+str(webhook.name)+"</li>"+"\n"
	print(html)
	return html

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
