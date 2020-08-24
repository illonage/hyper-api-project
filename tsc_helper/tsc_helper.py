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

import tableauserverclient as TSC
import requests
import urllib
import os

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
TABLEAU_SITE_NAME = os.environ.get('TABLEAU_SITE_NAME')
TABLEAU_TOKEN_NAME = os.environ.get('TABLEAU_TOKEN_NAME')
HEROKU_URL = "https://" + str(os.environ.get('HEROKU_APP_NAME')) + ".herokuapp.com/webhook"
TABLEAU_SERVER = 'https://10ax.online.tableau.com'
# TABLEAU_EVENT_NAME = os.environ.get('TABLEAU_EVENT_NAME')
# TABLEAU_TOKEN = "7FrN4uZlT3G9zIB714aSYQ==:7MpIUqGxreEd8GIlm0AC7Sb0nd0GrZ47"
# TABLEAU_SITE_NAME = "datadevdev247636"
# TABLEAU_TOKEN_NAME = "token"


def get_webhooks(token):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
        personal_access_token=token, site_id=TABLEAU_SITE_NAME)
    server = TSC.Server(TABLEAU_SERVER)

    # Set http options to disable verifying SSL
    server.add_http_options({'verify': False})
    server.use_server_version()
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        webhooks = []
        for webhook in TSC.Pager(server.webhooks):
            webhooks.append(webhook)

    return webhooks


def create_webhook(token, event_type):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
        personal_access_token=token, site_id=TABLEAU_SITE_NAME)
    server = TSC.Server(TABLEAU_SERVER)

    # Set http options to disable verifying SSL
    server.add_http_options({'verify': False})
    server.use_server_version()
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        new_webhook = TSC.WebhookItem()
        new_webhook.name = "Webooks created from Heroku"
        new_webhook.url = HEROKU_URL
        new_webhook.event = event_type

        # Check if identical webhook is already created
        exists = False
        for existing_webhook in TSC.Pager(server.webhooks):
            exists = compare_webhook(new_webhook, existing_webhook)
            if exists:
                break

        if not exists:
            new_webhook = server.webhooks.create(new_webhook)
            print("Webhook created: {}".format(new_webhook))
            return True, new_webhook
        else:
            print("Webhook already exists: {}".format(new_webhook))
            return False, new_webhook


def delete_webhook(token, id):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
        personal_access_token=token, site_id=TABLEAU_SITE_NAME)
    server = TSC.Server(TABLEAU_SERVER)

    # Set http options to disable verifying SSL
    server.add_http_options({'verify': False})
    server.use_server_version()
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        server.webhooks.delete(id)


def compare_webhook(new_webhook, existing_webhook):
    return (new_webhook.url == existing_webhook.url) and (new_webhook.event == existing_webhook.event)
