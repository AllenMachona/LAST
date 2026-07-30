from app import db
from models.notification import Notification
from datetime import datetime
import pytz

def create_notification(user_id, title, message, notification_type, procurement_id=None, action_url=None):
    n = Notification(
        user_id=user_id, title=title, message=message, notification_type=notification_type,
        procurement_id=procurement_id, action_url=action_url,
        created_at=datetime.now(pytz.timezone('Africa/Gaborone'))
    )
    db.session.add(n)
    db.session.commit()
    return n

def notify_procurement_users(procurement_id, title, message, notification_type):
    from models.procurement import Procurement
    p = Procurement.query.get(procurement_id)
    if p and p.created_by_user:
        create_notification(p.created_by_user.id, title, message, notification_type, procurement_id)
