import logging
import asyncio
from aiosmtpd.smtp import Envelope, Session, SMTP
import email
from email.policy import default
from enum import Enum
from typing import List

from common.config import SMTPConfig
from messaging.slack import SlackMessages

log = logging.getLogger(__name__)


class Responses(Enum):
    """SMTP responses."""
    ok = "250 OK"
    message_accepted = "250 Message accepted for delivery"


class NotifierHandler:
    """Handler used to send notification emails to Slack."""

    def __init__(self, config: SMTPConfig) -> None:
        self.config = config

    async def handle_RCPT(self, server: SMTP, session: Session, envelope: Envelope, address: str, rcpt_options: List[str]) -> str:
        """Checks message at the RCPT stage to make sure it is from the configured
        `INCOMING_EMAIL` address.  If not, the message is rejected."""
        if not address == self.config.incoming_email:
            return '541 Message rejected by the recipient address'

        log.info(f"Message received from {address}.")

        envelope.rcpt_tos.append(address)

        return Responses.ok.value

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope) -> str:
        """Gets the content of an email message and sends it to Slack."""
        try:
            message = self._parse_message(envelope)
        except ValueError:
            return '554, "5.6.0", Mail message is malformed. Not accepted.'

        log.debug(f"Subject: {message['subject']}")
        log.debug(f"Body: {message['body']}")

        slack = SlackMessages(self.config)
        slack.send_message(message)

        return Responses.message_accepted.value

    def _parse_message(self, envelope: Envelope) -> dict:
        """Get relevant data from an email."""
        if envelope.original_content is None:
            log.debug("Mail message has no content.")
            raise ValueError

        message = email.message_from_bytes(envelope.original_content, policy=default)
        message_from = message.get("From")
        subject = message.get("Subject")
        body = message.get_content().strip()

        return {'from': message_from, 'subject': subject, 'body': body}
