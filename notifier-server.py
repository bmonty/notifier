import sys
import logging
import signal

from messaging.slack import SlackMessages
from common.config import SMTPConfig
import smtp.server as smtp_server


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)
log = logging.getLogger()


def start_notifier():
    log.info("Starting Notifier.")

    # load config
    config = SMTPConfig()
    
    # create the singleton SlackMessages object and test the connection to Slack
    slack = SlackMessages(config)
    if not slack.test_connection():
        log.fatal("Unable to connect to Slack with the provided tokens.")
        sys.exit(1)

    # start servers
    controller = smtp_server.start_smtp_server(config)

    sig = signal.sigwait([signal.SIGINT, signal.SIGQUIT])

    # shutdown servers    
    log.info("Stopping Notifier.")
    smtp_server.stop_smtp_server(controller)


if __name__ == "__main__":
    start_notifier()
