import logging
from aiosmtpd.controller import Controller

from common.config import SMTPConfig
from smtp.smtp_handlers import NotifierHandler


log = logging.getLogger()


def start_smtp_server(config: SMTPConfig) -> Controller:
    """Starts the SMTP server to handle incoming notifications."""
    handler = NotifierHandler(config)

    controller = Controller(
        handler, hostname=config.hostname, port=config.port, ready_timeout=5)
    
    log.info(f"Starting SMTP server on port {config.port}.")
    controller.start()
    
    return controller

def stop_smtp_server(controller: Controller) -> None:
    """Stops the SMTP server."""
    log.info("Stopping SMTP server.")
    controller.stop()
