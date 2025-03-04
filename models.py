from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    messages = db.relationship('MessageHistory', backref='user', lazy=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'sms', 'email', 'bot'
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'sms', 'email', 'bot'
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'sent', 'failed', 'delivered'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sms_count = db.Column(db.Integer, default=0)
    email_count = db.Column(db.Integer, default=0)
    bot_messages_count = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    errors_count = db.Column(db.Integer, default=0)
