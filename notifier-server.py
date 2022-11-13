import logging
import signal

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
    
    # start servers
    controller = smtp_server.start_smtp_server(config)

    sig = signal.sigwait([signal.SIGINT, signal.SIGQUIT])

    # shutdown servers    
    log.info("Stopping Notifier.")
    smtp_server.stop_smtp_server(controller)


if __name__ == "__main__":
    start_notifier()
