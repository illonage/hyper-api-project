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
try:
    TOKEN = os.environ.get('SLACK_TOKEN')
    TABLEAU_TOKEN = os.environ.get('TABLEAU_TOKEN')
    TABLEAU_SITE_NAME = os.environ.get('TABLEAU_SITE_NAME')
    TABLEAU_TOKEN_NAME = os.environ.get('TABLEAU_TOKEN_NAME')
    TABLEAU_EVENT_NAME = os.environ.get('TABLEAU_EVENT_NAME')
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
except:
    MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
    TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'


def main():

    # SIGN IN
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=TABLEAU_TOKEN_NAME,
                                               personal_access_token=TABLEAU_TOKEN, site_id=TABLEAU_SITE_NAME)

    server = TSC.Server('https://10ax.online.tableau.com')

    # Set http options to disable verifying SSL
    server.add_http_options({'verify': False})
    server.use_server_version()

    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        new_webhook = TSC.WebhookItem()
        new_webhook.name = "Webooks created from Heroku"
        new_webhook.url = "https://"+str(HEROKU_APP_NAME)+".herokuapp.com/webhook/"
        new_webhook.event = TABLEAU_EVENT_NAME

        # Check if identical webhook is already created
        exists = False
        for existing_webhook in TSC.Pager(server.webhooks):
            exists = compare_webhook(new_webhook, existing_webhook)

        if not exists:
            new_webhook = server.webhooks.create(new_webhook)
            print("Webhook created: {}".format(new_webhook))

            # Gets all webhook items
            all_webhooks, pagination_item = server.webhooks.get()
            print("\nThere are {} webhooks on site: ".format(pagination_item.total_available))
            print([webhook.name for webhook in all_webhooks])
        else:
            print("Webhook already exists: {}".format(new_webhook))


def compare_webhook(new_webhook, existing_webhook):
    return (new_webhook.url == existing_webhook.url) and (new_webhook.event == existing_webhook.event)


if __name__ == '__main__':
    main()