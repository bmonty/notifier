import os
import json

from flask import Flask, request
import requests


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_prefixed_env("SYNOLOGY_NOTIFIER")

    @app.route("/")
    def hello():
        return "Hello!"

    @app.route("/notify", methods=["POST"])
    def notify():
        """Receives notifications from the Synology NAS and forwards the message to Slack."""
        # get slack info from the app config
        slack_url = app.config["SLACK_URL"]
        slack_channel = app.config["SLACK_CHANNEL"]

        # get message from the request arguments
        message = request.args.get("message", "")
        if message == "":
            return("No Message to Send")

        headers = {"content-type": "application/json"}
        data = {"text": message, "channel": slack_channel}

        r = requests.post(slack_url, headers=headers, data=json.dumps(data))
    
        return("OK")

    return app
