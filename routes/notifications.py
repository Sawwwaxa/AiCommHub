from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models import db, Notification, MessageHistory, Statistics

notifications = Blueprint('notifications', __name__)

@notifications.route('/api/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        read=False
    ).order_by(Notification.created_at.desc()).all()
    
    return jsonify([{
        'id': n.id,
        'type': n.type,
        'message': n.message,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@notifications.route('/api/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    notification_ids = request.json.get('notification_ids', [])
    Notification.query.filter(
        Notification.id.in_(notification_ids)
    ).update({Notification.read: True}, synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'success'})

@notifications.route('/api/history')
@login_required
def get_history():
    days = request.args.get('days', 7, type=int)
    history = MessageHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(MessageHistory.created_at.desc()).limit(100).all()
    
    return jsonify([{
        'id': h.id,
        'type': h.type,
        'content': h.content,
        'status': h.status,
        'created_at': h.created_at.isoformat()
    } for h in history])

@notifications.route('/api/statistics')
@login_required
def get_statistics():
    days = request.args.get('days', 7, type=int)
    stats = Statistics.query.order_by(Statistics.date.desc()).limit(days).all()
    
    return jsonify([{
        'date': s.date.isoformat(),
        'sms_count': s.sms_count,
        'email_count': s.email_count,
        'bot_messages_count': s.bot_messages_count,
        'active_users': s.active_users,
        'errors_count': s.errors_count
    } for s in stats])
