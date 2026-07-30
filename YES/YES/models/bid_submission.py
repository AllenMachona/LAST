from app import db
from datetime import datetime
import pytz

class BidSubmission(db.Model):
    __tablename__ = 'bid_submissions'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidders.id'), nullable=False)
    lot_id = db.Column(db.Integer)  # if multi-lot

    # Submission envelope
    envelope_type = db.Column(db.String(50), nullable=False)  # single, technical, financial

    # Files
    file_name = db.Column(db.String(500))
    file_path = db.Column(db.String(1000))
    file_size = db.Column(db.BigInteger)
    file_hash = db.Column(db.String(128))

    # Encryption
    encrypted = db.Column(db.Boolean, default=True)
    encryption_key_id = db.Column(db.String(200))

    # Status
    status = db.Column(db.String(50), default='draft')  # draft, submitted, withdrawn, replaced, late
    is_final = db.Column(db.Boolean, default=False)

    # Timestamps
    submitted_at = db.Column(db.DateTime)
    server_timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    receipt_number = db.Column(db.String(100), unique=True)

    # Withdrawal/Replacement
    withdrawn_at = db.Column(db.DateTime)
    withdrawal_reason = db.Column(db.Text)
    replaced_by_id = db.Column(db.Integer, db.ForeignKey('bid_submissions.id'))

    # Opening
    opened_at = db.Column(db.DateTime)
    opened_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    opening_batch_id = db.Column(db.Integer, db.ForeignKey('bid_openings.id'))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='bid_submissions')
    bidder = db.relationship('Bidder', back_populates='submissions')
    opener = db.relationship('User', foreign_keys=[opened_by])
    opening_batch = db.relationship('BidOpening', back_populates='submissions')
    replaced_by = db.relationship('BidSubmission', remote_side=[id])

    def __repr__(self):
        return f'<BidSubmission {self.receipt_number}>'
