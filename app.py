import requests
import json
import os
import re
import sys
import tableauserverclient as TSC
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tsc_helper.tsc_helper import create_webhook, delete_webhook, get_webhooks
from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = os.urandom(24)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@app.route('/', methods=['GET'])
def index():
    webhooks = get_webhooks(os.environ.get('TABLEAU_TOKEN'))
    return render_template('index.html', webhooks=webhooks)


@app.route('/create', methods=['POST'])
def create():
    token = request.form['token']
    event_type = request.form['event-type']
    if not event_type or not token:
        flash("Incomplete create request: event-type and/or token were not provided!")
    else:
        created, new_webhook = create_webhook(token, event_type)
        if created:
            flash("Webhook created: {}".format(new_webhook))
        else:
            flash("Webhook already exists: {}".format(new_webhook))

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    token = request.form['token']
    webhook_id = request.form['webhook-id']
    if not webhook_id or not token:
        flash("Incomplete delete request: event-type and/or token were not provided!")
    else:
        delete_webhook(token, webhook_id)
        flash("Webhook {} deleted.".format(webhook_id))

    return redirect(url_for('index'))

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
