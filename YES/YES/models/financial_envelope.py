from app import db
from datetime import datetime
import pytz

class FinancialEnvelope(db.Model):
    __tablename__ = 'financial_envelopes'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('bid_submissions.id'), nullable=False)

    # Content
    file_name = db.Column(db.String(500))
    file_path = db.Column(db.String(1000))
    file_hash = db.Column(db.String(128))

    # Encryption
    encrypted = db.Column(db.Boolean, default=True)
    decryption_key_part = db.Column(db.String(500))

    # Status
    status = db.Column(db.String(50), default='sealed')  # sealed, opened, evaluated
    opened_at = db.Column(db.DateTime)
    opened_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Financial data (extracted after opening)
    bid_amount = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3), default='BWP')
    validity_days = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    submission = db.relationship('BidSubmission', backref='financial_envelope', uselist=False)
    opener = db.relationship('User', foreign_keys=[opened_by])
