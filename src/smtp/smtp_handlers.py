from aiosmtpd.smtp import Envelope, Session, SMTP
from typing import List

from common.config import SMTPConfig


class NotifierHandler:
    """Handler used to send notification emails to Slack."""

    def __init__(self, config: SMTPConfig) -> None:
        self.config = config

    async def handle_RCPT(self, server: SMTP, session: Session, envelope: Envelope, address: str, rcpt_options: List[str]) -> str:
        """Checks message at the RCPT stage to make sure it is from the configured
        `INCOMING_EMAIL` address.  If not, the message is rejected."""
        if not address == self.config.incoming_email:
            return '541 Message rejected by the recipient address'

        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope) -> str:
        """Gets the content of an email message and sends it to Slack."""
        return '250 Message accepted for delivery'
