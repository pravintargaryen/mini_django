# test_mail.py

from unittest.mock import patch, MagicMock

from mini_django import send_mail


@patch("mini_django.core.mail.smtplib.SMTP")
def test_send_mail(mock_smtp):

    connection = MagicMock()
    mock_smtp.return_value.__enter__.return_value = connection

    send_mail(
        email="test@gmail.com",
        password="password",
        subject="Test subject",
        message="Hello from pytest",
        from_address="test@gmail.com",
        to_address=["receiver@gmail.com"]
    )

    mock_smtp.assert_called_once_with(
        "smtp.gmail.com",
        port=587
    )

    connection.starttls.assert_called_once()

    connection.login.assert_called_once_with(
        user="test@gmail.com",
        password="password"
    )

    connection.sendmail.assert_called_once_with(
        from_addr="test@gmail.com",
        to_address=["receiver@gmail.com"]
    )