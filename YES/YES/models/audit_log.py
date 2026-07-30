from app import db
from datetime import datetime
import pytz

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)

    # Actor
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_role = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    device_session = db.Column(db.String(200))

    # Action
    action = db.Column(db.String(100), nullable=False, index=True)
    action_category = db.Column(db.String(50))  # create, read, update, delete, login, export, open, evaluate

    # Object
    object_type = db.Column(db.String(50))  # procurement, bid, evaluation, award, etc.
    object_id = db.Column(db.Integer)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'))

    # Data
    previous_value = db.Column(db.JSON)
    new_value = db.Column(db.JSON)
    reason = db.Column(db.Text)

    # Integrity
    hash_value = db.Column(db.String(128))
    signature = db.Column(db.String(256))

    # Timestamp
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')), index=True)

    # Severity
    severity = db.Column(db.String(20), default='info')  # info, warning, critical

    # Relationships
    user = db.relationship('User', back_populates='audit_logs')
    procurement = db.relationship('Procurement', back_populates='audit_logs')

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'
