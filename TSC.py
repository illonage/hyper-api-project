####
# This script demonstrates how to use the Tableau Server Client
# to interact with webhooks. It explores the different
# functions that the Server API supports on webhooks.
#
# With no flags set, this sample will query all webhooks,
# pick one webhook and print the name of the webhook.
# Adding flags will demonstrate the specific feature
# on top of the general operations.
####

import argparse
import getpass
import logging
import os.path

import tableauserverclient as TSC


import websocket
import json
import requests
import urllib
import os
import sys
import logging
c


logging.basicConfig(level=logging.DEBUG,
        stream=sys.stdout)

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        TOKEN = os.environ.get('SLACK_TOKEN')
        TABLEAU_TOKEN = os.environ.get('TABLEAU_TOKEN')
        TABLEAU_SITE_NAME = os.environ.get('TABLEAU_SITE_NAME')
	    TABLEAU_TOKEN_NAME = os.environ.get('TABLEAU_TOKEN_NAME')
        TABLEAU_EVENT_NAME = os.environ.get('TABLEAU_EVENT_NAME')
        DEBUG_CHANNEL_ID = os.environ.get('DEBUG_CHANNEL_ID', False)
except:
        MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
        TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'
        UNFURL = 'FALSE'


def main():

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, DEBUG)
    logging.basicConfig(level=debug)

    # SIGN IN
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
                                                   personal_access_token=TABLEAU_TOKEN, site_id=TABLEAU_SITE_NAME)

    # Set http options to disable verifying SSL
    server.add_http_options({'verify': False})

    server.use_server_version()

    with server.auth.sign_in_with_personal_access_token(tableau_auth):

        # Create webhook if create flag is set (-create, -c)

        new_webhook = TSC.WebhookItem()
        new_webhook.name = "Webooks created from Heroku"
        new_webhook.url = "https://webhook.site/c0958e0a-ad1d-493b-97bb-7344586684a5"
        new_webhook.event = TABLEAU_EVENT_NAME
        print(new_webhook)
        new_webhook = server.webhooks.create(new_webhook)
        print("Webhook created. ID: {}".format(new_webhook.id))

        # Gets all webhook items
        all_webhooks, pagination_item = server.webhooks.get()
        print("\nThere are {} webhooks on site: ".format(pagination_item.total_available))
        print([webhook.name for webhook in all_webhooks])

        if all_webhooks:
            # Pick one webhook from the list and delete it
            sample_webhook = all_webhooks[0]
            # sample_webhook.delete()
            print("+++"+sample_webhook.name)



if __name__ == '__main__':
    main()