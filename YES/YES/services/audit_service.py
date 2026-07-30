from app import db
from models.audit_log import AuditLog
from datetime import datetime
import pytz

def log_audit(user_id, action, object_type, object_id, procurement_id=None, reason=None, previous_value=None, new_value=None):
    log = AuditLog(
        user_id=user_id, action=action, object_type=object_type, object_id=object_id,
        procurement_id=procurement_id, reason=reason, previous_value=previous_value,
        new_value=new_value, timestamp=datetime.now(pytz.timezone('Africa/Gaborone')), severity='info'
    )
    db.session.add(log)
    db.session.commit()
    return log
