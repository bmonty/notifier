import pytest

from common.config import SMTPConfig
from smtp.smtp_handlers import NotifierHandler


@pytest.mark.asyncio
async def test_smtp_notifier_handle_rcpt(monkeypatch, mocker) -> None:
    """Test the RCPT handler recognizes the configured incoming email."""
    monkeypatch.setenv("NOTIFIER_INCOMING_EMAIL", "test@example.com")
    envelope = mocker.MagicMock()

    config = SMTPConfig()
    handler = NotifierHandler(config)
    response = await handler.handle_RCPT(None, None, envelope, 'test@example.com', None)

    assert '250 OK' == response
    envelope.rcpt_tos.append.assert_called_with('test@example.com')


@pytest.mark.asyncio
async def test_smtp_notifier_handle_rcpt_fails(monkeypatch, mocker) -> None:
    """Test the RCPT handler rejects messages not sent to the configured incoming email."""
    monkeypatch.setenv("NOTIFIER_INCOMING_EMAIL", "test@example.com")
    envelope = mocker.MagicMock()

    config = SMTPConfig()
    handler = NotifierHandler(config)
    response = await handler.handle_RCPT(None, None, envelope, 'fail@example.com', None)

    assert '541 Message rejected by the recipient address' == response
    envelope.rcpt_tos.append.assert_not_called()
