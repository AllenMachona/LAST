from app import db
from datetime import datetime
import pytz

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'))

    # Content
    title = db.Column(db.String(300), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # tender_published, bid_opening, evaluation, award, complaint, system

    # Channels
    in_app = db.Column(db.Boolean, default=True)
    email_sent = db.Column(db.Boolean, default=False)
    sms_sent = db.Column(db.Boolean, default=False)

    # Status
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)

    # Action link
    action_url = db.Column(db.String(500))
    action_text = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    user = db.relationship('User', back_populates='notifications')
    procurement = db.relationship('Procurement', back_populates='notifications')

    def __repr__(self):
        return f'<Notification {self.title}>'

    def mark_read(self):
        self.read = True
        self.read_at = datetime.now(pytz.timezone('Africa/Gaborone'))
