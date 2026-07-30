from app import db
from datetime import datetime
import pytz

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    activity = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)

    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    def __repr__(self):
        return f'<ActivityLog {self.activity}>'
