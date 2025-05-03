import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from typing import Optional

from app.exceptions import EmailException
from app.settings import api_settings


class EmailService:
    @staticmethod
    def send_confirmation_email(email_to: str, token: str) -> bool:
        """Отправка email с подтверждением регистрации"""
        try:
            confirmation_link = (
                f"{api_settings.API_BASE_URL}/confirm-email?token={token}"
            )
            message = f"""
            Подтвердите ваш email, перейдя по ссылке:
            {confirmation_link}

            Ссылка действительна {api_settings.EMAIL_CONFIRMATION_EXPIRE_HOURS} часов.
            """

            msg = MIMEText(message)
            msg['Subject'] = 'Подтверждение email'
            msg['From'] = api_settings.SMTP_FROM
            msg['To'] = email_to

            with smtplib.SMTP(api_settings.SMTP_HOST, api_settings.SMTP_PORT) as server:
                server.starttls()
                server.login(api_settings.SMTP_USER, api_settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            raise EmailException(f"Failed to send confirmation email: {str(e)}")

    @staticmethod
    def send_password_reset_email(email_to: str, token: str) -> bool:
        """Отправка email для сброса пароля"""
        try:
            reset_link = f"{api_settings.API_BASE_URL}/reset-password?token={token}"
            message = f"""
            Для сброса пароля перейдите по ссылке:
            {reset_link}

            Ссылка действительна {api_settings.ACCESS_TOKEN_EXPIRE_MINUTES} минут.
            """

            msg = MIMEText(message)
            msg['Subject'] = 'Сброс пароля'
            msg['From'] = api_settings.SMTP_FROM
            msg['To'] = email_to

            with smtplib.SMTP(api_settings.SMTP_HOST, api_settings.SMTP_PORT) as server:
                server.starttls()
                server.login(api_settings.SMTP_USER, api_settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            raise EmailException(f"Failed to send password reset email: {str(e)}")


# Функции-обертки для удобного импорта
async def send_confirmation_email(email_to: str, token: str) -> bool:
    return EmailService.send_confirmation_email(email_to, token)


async def send_password_reset_email(email_to: str, token: str) -> bool:
    return EmailService.send_password_reset_email(email_to, token)