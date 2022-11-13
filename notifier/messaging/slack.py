import logging
import slack_sdk
import slack_sdk.errors

from common.config import Config


log = logging.getLogger()


class SlackMessages(object):
    """Class for managing notifications sent to Slack."""
    _channel_id_cache = {}

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = slack_sdk.WebClient(token=config.slack_bot_token)

    def test_connection(self) -> bool:
        # test the connection to Slack
        try:
            response = self.client.api_test()
        except slack_sdk.errors.SlackApiError:
            return False
        else:
            return True

    def send_message(self, message: dict) -> None:
        log.debug("Sending message to Slack.")
        channel_id = self._get_channel_id(self.config.slack_channel)
        response = self.client.chat_postMessage(
            channel=channel_id,
            text=f"Notification from {message['from']}.",
            blocks=self._make_message_blocks(message)
        )
        log.info(f"Message successfully sent to Slack.")

    def _get_channel_id(self, channel_name: str) -> str:
        """Converts a channel name to the Slack channel ID.  Channel IDs are cached with the instance."""
        if channel_name in self._channel_id_cache:
            return self._channel_id_cache[channel_name]

        response = self.client.conversations_list()
        for channel in response["channels"]:
            if channel["name"] == channel_name:
                self._channel_id_cache[channel_name] = channel["id"]
                return channel["id"]

        raise ValueError("Channel not found.")

    def _make_message_blocks(self, message) -> list:
        """Format a message using blocks."""
        blocks = []

        # add the subject
        blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*From:* {message['from']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Subject:* {message['subject']}"
                }
            ]
        })

        # add the message body
        blocks.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": message["body"]
            }
        })

        return blocks
