import os
import logging
from twilio.rest import Client

# Configure logging
logger = logging.getLogger(__name__)

def send_sms(to_number: str, message: str) -> bool:
    """
    Send SMS using Twilio

    Args:
        to_number: Recipient's phone number
        message: Message content

    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_PHONE_NUMBER")

        if not all([account_sid, auth_token, from_number]):
            logger.error("Missing Twilio credentials in environment variables")
            return False

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        logger.info(f"SMS sent successfully with SID: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False