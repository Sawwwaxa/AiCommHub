import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Configure logging
logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, content: str) -> bool:
    """
    Send email using SendGrid

    Args:
        to_email: Recipient's email address
        subject: Email subject
        content: Email content

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        api_key = os.environ.get("SENDGRID_API_KEY")
        from_email = os.environ.get("SENDGRID_FROM_EMAIL")

        if not all([api_key, from_email]):
            logger.error("Missing SendGrid credentials in environment variables")
            return False

        sg = SendGridAPIClient(api_key)

        message = Mail(
            from_email=Email(from_email),
            to_emails=To(to_email),
            subject=subject,
            content=Content("text/plain", content)
        )

        sg.send(message)
        logger.info(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False