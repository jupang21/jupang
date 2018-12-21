import _sendmessage as sendmessage
import json

from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

slack_token = 'testing'
slack_client_id = 'testing.507325084531'
slack_client_secret = 'testing'
slack_verification ='testing'
sc = SlackClient(slack_token)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event)
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = sendmessage.make_bot_respone(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords,
            attachments = [
                {
                    "author_name": "Stanford S. Strickland",
                    "image_url" : "http://blogfiles.naver.net/MjAxODExMDFfMjEg/MDAxNTQxMDU1MTI5Njky.Cc1i5dXldC167B3MHB-2XviBdv6ppRQyQ8C36zE8mGMg.a2_VFgojZfAiXNgnAjIFcXxG_aQWSFABpCwAklO8ZAIg.PNG.leemacin/%C0%CC%B9%CC%C1%F6_13.png"
                }
            ]
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

def hears():
    slack_event = json.loads(request.data)
    print(slack_event)
    
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})