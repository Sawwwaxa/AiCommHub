import os
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, current_user, UserMixin
from bot import setup_bot

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

# Initialize Telegram bot
bot = setup_bot()
if not bot:
    logger.warning("Bot not initialized - check TELEGRAM_BOT_TOKEN in environment variables")

# Dummy User model for demonstration
# In a production environment, you should implement a proper user model with database integration
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    """
    User loader function required by Flask-Login
    In a production environment, you would typically load the user from a database
    """
    try:
        return User(user_id)
    except Exception as e:
        logger.error(f"Error loading user: {e}")
        return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template(
        'index.html',
        firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
        firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
        firebase_app_id=os.environ.get("FIREBASE_APP_ID", "")
    )

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    # Vérifier si les services sont configurés
    services_status = {
        'telegram': bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
        'openai': bool(os.environ.get("OPENAI_API_KEY")),
        'twilio': bool(os.environ.get("TWILIO_ACCOUNT_SID")),
        'sendgrid': bool(os.environ.get("SENDGRID_API_KEY")),
        'firebase': bool(os.environ.get("FIREBASE_PROJECT_ID"))
    }

    return render_template('dashboard.html', services_status=services_status)

@app.route('/api/stats')
def get_stats():
    if not bot:
        return jsonify({
            'messages_processed': 0,
            'active_users': 0,
            'errors': 0,
            'status': 'Bot non configuré - Vérifiez TELEGRAM_BOT_TOKEN dans les variables d\'environnement',
            'services_status': {
                'telegram': bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
                'openai': bool(os.environ.get("OPENAI_API_KEY")),
                'twilio': bool(os.environ.get("TWILIO_ACCOUNT_SID")),
                'sendgrid': bool(os.environ.get("SENDGRID_API_KEY")),
                'firebase': bool(os.environ.get("FIREBASE_PROJECT_ID"))
            }
        })

    return jsonify({
        'messages_processed': bot.messages_processed,
        'active_users': len(bot.active_users),
        'errors': bot.error_count,
        'status': 'Bot actif',
        'services_status': {
            'telegram': True,
            'openai': bool(os.environ.get("OPENAI_API_KEY")),
            'twilio': bool(os.environ.get("TWILIO_ACCOUNT_SID")),
            'sendgrid': bool(os.environ.get("SENDGRID_API_KEY")),
            'firebase': bool(os.environ.get("FIREBASE_PROJECT_ID"))
        }
    })

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"An error occurred: {error}")
    return jsonify({'error': str(error)}), 500