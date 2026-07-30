from app import db
from datetime import datetime
import pytz

class Award(db.Model):
    __tablename__ = 'awards'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('bid_submissions.id'))
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidders.id'))

    # Award details
    award_type = db.Column(db.String(50), default='single')  # single, multiple_lots, framework
    lot_id = db.Column(db.Integer)

    # Financial
    contract_amount = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3), default='BWP')
    contract_duration = db.Column(db.Integer)  # days

    # Approval workflow
    recommendation_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    recommended_at = db.Column(db.DateTime)
    procurement_unit_approved = db.Column(db.Boolean, default=False)
    pou_approved = db.Column(db.Boolean, default=False)
    ao_approved = db.Column(db.Boolean, default=False)
    ao_approved_at = db.Column(db.DateTime)
    ao_approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Notification
    bidders_notified = db.Column(db.Boolean, default=False)
    notification_date = db.Column(db.DateTime)
    successful_bidder_letter = db.Column(db.String(1000))
    unsuccessful_bidder_letter = db.Column(db.String(1000))

    # Publication
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    publication_evidence = db.Column(db.String(1000))

    # Cooling-off
    cooling_off_started = db.Column(db.Boolean, default=False)
    cooling_off_start = db.Column(db.DateTime)
    cooling_off_end = db.Column(db.DateTime)
    cooling_off_observed = db.Column(db.Boolean, default=False)

    # Debriefing
    debriefing_available = db.Column(db.Boolean, default=True)
    debriefing_deadline = db.Column(db.DateTime)

    # Contract handover
    contract_ready = db.Column(db.Boolean, default=False)
    handover_package_generated = db.Column(db.Boolean, default=False)
    handover_package_path = db.Column(db.String(1000))

    # Status
    status = db.Column(db.String(50), default='recommended')  # recommended, approved, published, cooling_off, ready_for_contract, contracted, cancelled

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')),
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='awards')
    submission = db.relationship('BidSubmission')
    bidder = db.relationship('Bidder')
    recommender = db.relationship('User', foreign_keys=[recommendation_by])
    approver = db.relationship('User', foreign_keys=[ao_approved_by])

    def __repr__(self):
        return f'<Award {self.id}>'

    def is_cooling_off_active(self):
        if not self.cooling_off_end:
            return False
        now = datetime.now(pytz.timezone('Africa/Gaborone'))
        return now < self.cooling_off_end
