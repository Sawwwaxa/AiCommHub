import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials from environment variables"""
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
    })

    if not firebase_admin._apps:  # Only initialize if not already initialized
        try:
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            return False
    return True

def verify_user(user_id: str) -> bool:
    """Verify if a user exists in Firebase"""
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            if not initialize_firebase():
                return False

        # Verify the user exists in Firebase
        user = auth.get_user(user_id)
        return True
    except auth.UserNotFoundError:
        return False
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False