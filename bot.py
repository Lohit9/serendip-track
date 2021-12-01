import slack 
import os 
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask 
from slackeventsapi import SlackEventAdapter
import logging

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__) 
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN']) 
BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('app_home_opened')
def home(payload):
    print(payload)
    event = payload.get('event', {})
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Get ready to supercharge your network!* :rocket:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Answer the following to better prepare to meet new people."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          },
          {
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "title",
				"placeholder": {
					"type": "plain_text",
					"text": "What do you want to ask of the world?"
				}
			}
          }
        ]
      }
    )

@slack_event_adapter.on('message') 
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user') 
    text = event.get('text') 

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)


if __name__ == "__main__": 
    app.run(debug=True)