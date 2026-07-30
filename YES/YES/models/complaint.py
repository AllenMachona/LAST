from app import db
from datetime import datetime
import pytz

class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    award_id = db.Column(db.Integer, db.ForeignKey('awards.id'))

    # Complainant
    complainant_type = db.Column(db.String(50), nullable=False)  # bidder, public, other
    complainant_id = db.Column(db.Integer)  # Bidder ID if applicable
    complainant_name = db.Column(db.String(300))
    complainant_email = db.Column(db.String(120))

    # Complaint details
    complaint_form_data = db.Column(db.JSON)
    grounds = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.JSON)  # List of file references
    relief_sought = db.Column(db.Text)

    # Fee
    fee_paid = db.Column(db.Boolean, default=False)
    fee_amount = db.Column(db.Numeric(10, 2))
    fee_receipt = db.Column(db.String(500))

    # Timeline
    received_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    acknowledged_at = db.Column(db.DateTime)
    response_due = db.Column(db.DateTime)

    # Suspension
    suspension_requested = db.Column(db.Boolean, default=False)
    suspension_granted = db.Column(db.Boolean, default=False)
    suspension_start = db.Column(db.DateTime)
    suspension_end = db.Column(db.DateTime)

    # Review
    assigned_reviewer = db.Column(db.Integer, db.ForeignKey('users.id'))
    hearing_scheduled = db.Column(db.Boolean, default=False)
    hearing_date = db.Column(db.DateTime)
    hearing_notes = db.Column(db.Text)
    expert_input = db.Column(db.JSON)

    # Decision
    decision = db.Column(db.Text)
    decision_date = db.Column(db.DateTime)
    remedy = db.Column(db.Text)
    decision_issued_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Appeal
    appeal_filed = db.Column(db.Boolean, default=False)
    appeal_details = db.Column(db.JSON)
    tribunal_reference = db.Column(db.String(200))

    # Status
    status = db.Column(db.String(50), default='submitted')  # submitted, acknowledged, under_review, hearing_scheduled, decided, appealed, resolved, dismissed

    # Case file access
    case_file_restricted = db.Column(db.Boolean, default=True)
    access_granted_to = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')),
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='complaints')
    award = db.relationship('Award')
    reviewer = db.relationship('User', foreign_keys=[assigned_reviewer])
    decision_maker = db.relationship('User', foreign_keys=[decision_issued_by])

    def __repr__(self):
        return f'<Complaint {self.id}>'

    def is_active(self):
        return self.status not in ['resolved', 'dismissed']
