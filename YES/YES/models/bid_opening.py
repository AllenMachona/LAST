from app import db
from datetime import datetime
import pytz

class BidOpening(db.Model):
    __tablename__ = 'bid_openings'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)

    # Opening details
    opening_type = db.Column(db.String(50), nullable=False)  # public, virtual, live_streamed, private
    envelope_opened = db.Column(db.String(50), nullable=False)  # technical, financial, single

    # Panel
    panel_members = db.Column(db.JSON)  # List of user IDs and names
    quorum_met = db.Column(db.Boolean, default=False)

    # Form alignment (PPRA Forms G, H, I)
    form_type = db.Column(db.String(10))  # G, H, I
    form_data = db.Column(db.JSON)

    # Recording
    recording_url = db.Column(db.String(1000))
    attendance_sheet = db.Column(db.String(1000))

    # Decryption
    decryption_method = db.Column(db.String(100))  # multi_person_control, quorum
    key_holders_present = db.Column(db.JSON)

    # Status
    status = db.Column(db.String(50), default='scheduled')  # scheduled, in_progress, completed, cancelled

    scheduled_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='bid_openings')
    submissions = db.relationship('BidSubmission', back_populates='opening_batch')
    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f'<BidOpening {self.form_type} for {self.procurement_id}>'
