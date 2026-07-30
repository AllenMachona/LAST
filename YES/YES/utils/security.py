from app import db
from models.activity_log import ActivityLog
from datetime import datetime
import pytz

def log_activity(user_id, activity, description, entity_type=None, entity_id=None):
    log = ActivityLog(
        user_id=user_id, activity=activity, description=description,
        entity_type=entity_type, entity_id=entity_id,
        timestamp=datetime.now(pytz.timezone('Africa/Gaborone'))
    )
    db.session.add(log)
    db.session.commit()
