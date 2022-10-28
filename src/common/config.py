import os
from typing import Any, Optional


class Config(object):
    """Base class for accessing and storing application configuration."""

    def __init__(self, prefix: str = "NOTIFIER", config: Optional[dict] = None) -> None:
        # store initial config or create an empty dictionary
        if config:
            self.cached_config = config
        else:
            self.cached_config = {}

        self.prefix = prefix

    def get_property(self, property_name: str) -> Any:
        """Get a property from the environment.  If the property has already
        been retrieved it is returned from cache.  If the property doesn't exist
        in the environment, the method will raise a `RuntimeError`."""
        # check if property exists in cache
        if property_name in self.cached_config:
            return self.cached_config[property_name]

        # get the property from the environment
        property = os.getenv(f"{self.prefix}_{property_name}")

        if property is None:
            raise RuntimeError(f"{property_name} is not in the environment.")

        self.cached_config[property_name] = property
        return property

    def clear_cache(self) -> None:
        self.cached_config.clear()

    @property
    def slack_url(self) -> str:
        return self.get_property("SLACK_URL")

    @property
    def slack_channel(self) -> str:
        return self.get_property("SLACK_CHANNEL")


class SMTPConfig(Config):
    """Class for configuring the SMTP notifier."""

    @property
    def incoming_email(self) -> str:
        """Notifications must be sent to this address to
        be forwarded to Slack."""
        return self.get_property("INCOMING_EMAIL")

    @property
    def port(self) -> int:
        """Port to listen for SMTP connections."""
        try:
            # the port is returned from the environment and
            # stored in the cache as a string
            return int(self.get_property("SMTP_PORT"))

        except RuntimeError:
            self.cached_config["SMTP_PORT"] = 25
            return 25

    @property
    def address(self) -> str:
        """Address to listen on.  Defaults to localhost
        (127.0.0.1)."""
        try:
            return self.get_property("SMTP_ADDRESS")

        except RuntimeError:
            self.cached_config["SMTP_ADDRESS"] = "127.0.0.1"
            return "127.0.0.1"
