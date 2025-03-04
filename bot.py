import os
import logging
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from services.firebase_service import verify_user
from services.openai_service import process_message
from services.twilio_service import send_sms
from services.sendgrid_service import send_email

logger = logging.getLogger(__name__)

HELP_MESSAGE = """
🤖 Bienvenue sur AICommHub! 

Voici les commandes disponibles:

📱 Envoi de SMS:
/sms [numéro] [message]
Exemple: /sms +33612345678 Bonjour!

📧 Envoi d'Email:
/email [destinataire] [sujet] [message]
Exemple: /email user@example.com "Mon sujet" Mon message

🔐 Authentification:
/auth - Pour accéder aux fonctionnalités

💡 IA Conversation:
Envoyez simplement un message pour discuter avec l'IA

❓ Aide:
/help - Afficher ce message d'aide
"""

class TelegramBot:
    def __init__(self):
        self.messages_processed = 0
        self.active_users = set()
        self.error_count = 0
        self.application = None
        self._stop_event = threading.Event()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /start"""
        await update.message.reply_text(
            f'👋 Bienvenue sur AICommHub!\n\n'
            f'Pour commencer, utilisez /auth pour vous authentifier.\n'
            f'Utilisez /help pour voir toutes les commandes disponibles.'
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /help"""
        await update.message.reply_text(HELP_MESSAGE)

    async def auth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /auth"""
        user_id = update.effective_user.id
        if verify_user(str(user_id)):
            self.active_users.add(user_id)
            await update.message.reply_text(
                '✅ Authentification réussie!\n\n'
                'Vous pouvez maintenant utiliser toutes les fonctionnalités du bot.\n'
                'Envoyez /help pour voir la liste des commandes.'
            )
        else:
            await update.message.reply_text(
                '❌ Échec de l\'authentification.\n'
                'Veuillez vérifier vos identifiants et réessayer.'
            )

    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire des messages texte normaux"""
        try:
            if update.effective_user.id not in self.active_users:
                await update.message.reply_text(
                    '🔒 Veuillez vous authentifier d\'abord avec /auth\n'
                    'Utilisez /help pour plus d\'informations.'
                )
                return

            # Process message with OpenAI
            response = process_message(update.message.text)

            # Send response via Telegram
            await update.message.reply_text(response)

            self.messages_processed += 1

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.error_count += 1
            await update.message.reply_text('Une erreur est survenue lors du traitement de votre message.')

    async def send_sms_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /sms"""
        if not os.environ.get("TWILIO_ACCOUNT_SID"):
            await update.message.reply_text('⚠️ Service SMS non configuré')
            return

        if len(context.args) < 2:
            await update.message.reply_text(
                '📱 Usage: /sms numéro message\n'
                'Exemple: /sms +33612345678 Bonjour!'
            )
            return

        phone_number = context.args[0]
        message = ' '.join(context.args[1:])

        try:
            if send_sms(phone_number, message):
                await update.message.reply_text('✅ SMS envoyé avec succès!')
            else:
                await update.message.reply_text('❌ Échec de l\'envoi du SMS.')
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            await update.message.reply_text('❌ Échec de l\'envoi du SMS.')

    async def send_email_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestionnaire de la commande /email"""
        if not os.environ.get("SENDGRID_API_KEY"):
            await update.message.reply_text('⚠️ Service email non configuré')
            return

        if len(context.args) < 3:
            await update.message.reply_text(
                '📧 Usage: /email destinataire sujet message\n'
                'Exemple: /email user@example.com "Mon sujet" Mon message'
            )
            return

        recipient = context.args[0]
        subject = context.args[1]
        message = ' '.join(context.args[2:])

        try:
            if send_email(recipient, subject, message):
                await update.message.reply_text('✅ Email envoyé avec succès!')
            else:
                await update.message.reply_text('❌ Échec de l\'envoi de l\'email.')
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            await update.message.reply_text('❌ Échec de l\'envoi de l\'email.')

    def stop_bot(self):
        """Arrêter le bot proprement"""
        self._stop_event.set()
        if self.application:
            self.application.stop()

    def run_polling(self):
        """Exécuter le polling dans un thread séparé"""
        try:
            self.application.run_polling()
        except Exception as e:
            logger.error(f"Error in polling thread: {e}")
            self.error_count += 1

def setup_bot():
    """Configure et démarre le bot Telegram"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Token du bot Telegram non trouvé dans les variables d'environnement")
        return None

    try:
        bot = TelegramBot()
        application = Application.builder().token(token).build()

        # Register handlers
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("help", bot.help))
        application.add_handler(CommandHandler("auth", bot.auth))
        application.add_handler(CommandHandler("sms", bot.send_sms_command))
        application.add_handler(CommandHandler("email", bot.send_email_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.process_message))

        bot.application = application

        # Start polling in a separate thread
        polling_thread = threading.Thread(target=bot.run_polling, daemon=True)
        polling_thread.start()

        return bot
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du bot: {e}")
        return None