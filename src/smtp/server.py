from aiosmtpd.controller import Controller

from common.config import SMTPConfig
from smtp.smtp_handlers import NotifierHandler


def start_smtp_server(config: SMTPConfig) -> None:
    """Starts the SMTP server to handle incoming notifications."""
    handler = NotifierHandler(config)
    
    controller = Controller(handler)
    controller.start()
