import json
import requests

from common.config import Config


def send_to_slack(config: Config, message: dict) -> None:
    """Sends a message to Slack."""
    headers = {"content-type": "application/json"}
    data = {"text": message["body"], "channel": config.slack_channel}

    r = requests.post(config.slack_url, headers=headers, data=json.dumps(data))
