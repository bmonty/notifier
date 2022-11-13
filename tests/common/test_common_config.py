import pytest

from common.config import Config, SMTPConfig


def test_config_init_with_initial_values():
    """Test a Config object can be initialized with values in the cache."""
    init_config = {'a': 1, 'b': 2, 'c': 3}
    config = Config(config=init_config)

    assert hasattr(config, 'cached_config')
    assert config.cached_config == init_config


def test_config_slack_properties(monkeypatch) -> None:
    """Test a Config object can object config values from the environment
    and store them in the cache."""
    monkeypatch.setenv("NOTIFIER_SLACK_URL", "test1")
    monkeypatch.setenv("NOTIFIER_SLACK_CHANNEL", "test2")

    config = Config()

    assert config.slack_url == "test1"
    assert config.slack_channel == "test2"
    assert "SLACK_URL" in config.cached_config
    assert "SLACK_CHANNEL" in config.cached_config


def test_config_missing_slack_envvar_throws_error(monkeypatch) -> None:
    """Test a request for a configuration value that doesn't exist throws
    a `RuntimeError`."""
    monkeypatch.delenv("NOTIFIER_SLACK_URL", raising=False)

    config = Config()

    with pytest.raises(RuntimeError):
        config.slack_url
    assert "SLACK_URL" not in config.cached_config


def test_config_custom_prefix(monkeypatch) -> None:
    """Test a Config object can get values from the environment using a custom prefix."""
    monkeypatch.setenv("TEST_SLACK_URL", "test")

    config = Config(prefix="TEST")

    assert config.slack_url == "test"


def test_config_get_property_from_cache() -> None:
    """Test a Config object returns a value from the cache instead of
    checking the environment."""
    config = Config(config={"SLACK_URL": "test"})

    # this will throw if the value isn't in the cache
    assert config.slack_url == "test"


# SMTP CONFIG


def test_smtp_config_incoming_email_property(monkeypatch) -> None:
    """Test a `SMTPConfig` object can return the incoming email property."""
    monkeypatch.setenv("NOTIFIER_INCOMING_EMAIL", "test")

    config = SMTPConfig()

    assert config.incoming_email == "test"


def test_smtp_config_default_port(monkeypatch) -> None:
    """Test a `SMTPConfig` object can return the default SMTP port value."""
    monkeypatch.delenv("NOTIFIER_SMTP_PORT", raising=False)

    config = SMTPConfig()

    assert config.port == 20025
    assert config.cached_config["SMTP_PORT"] == 20025


def test_smtp_config_custom_port(monkeypatch) -> None:
    """Test a `SMTPConfig` object can return a port value from the environment."""
    monkeypatch.setenv("NOTIFIER_SMTP_PORT", "69")

    config = SMTPConfig()

    assert config.port == 69
    assert config.cached_config["SMTP_PORT"] == "69"


def test_smtp_config_default_address() -> None:
    """Test a `SMTPConfig` object can return the default listen address."""
    config = SMTPConfig()

    assert config.hostname == "localhost"
    assert config.cached_config["SMTP_HOSTNAME"] == "localhost"


def test_smtp_config_custom_address(monkeypatch) -> None:
    """Test a `SMTPConfig` object can return a listen address from the environment."""
    monkeypatch.setenv("NOTIFIER_SMTP_HOSTNAME", "0.0.0.0")

    config = SMTPConfig()

    assert config.hostname == "0.0.0.0"
    assert config.cached_config["SMTP_HOSTNAME"] == "0.0.0.0"
