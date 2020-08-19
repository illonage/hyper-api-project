# Tableau Slackhooks
We are using Heroku to set up a Destination Server for our Tableau Webhooks.

### Set up Slack to send messages using Incoming Webhooks
All the instructions can be found on the [Slack website](!https://api.slack.com/messaging/webhooks).

Once you have created a Slack app, copy and paste your webhook URL in a safe space. It should look like this: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX You will need it later.

### Sign up for the Tableau Developer Program, and get your free Developer Site
Sign up for the Tableau Developer Program [here](!https://www.tableau.com/developer), and [get your free Developer Site](!https://www.tableau.com/developer/get-site)

### Create your Personal Access Token
Personal access tokens provide Tableau users the ability to create long-lived authentication tokens. Follow the instrucrion on the [Tableau Webiste](!https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm). You will need the Token name, and Token.

### Create a Heroku Account 
Create a Heroku Account [here](!https://signup.heroku.com/)

### Deploy Webhooks on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Switch your app to Online
Once the app is deployed:
1. Click on Manage App
2. Click on Resources
3. Under Free Dynos, switch the toggle button on for the worker so it looks blue, then press confirm.



