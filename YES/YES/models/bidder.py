from app import db
from datetime import datetime
import pytz

class Bidder(db.Model):
    __tablename__ = 'bidders'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)

    # Company info
    company_name = db.Column(db.String(300), nullable=False)
    registration_number = db.Column(db.String(100))
    tax_id = db.Column(db.String(100))
    ppra_registration_code = db.Column(db.String(50))
    ppra_grade = db.Column(db.String(20))

    # Ownership
    ownership_category = db.Column(db.String(100))  # citizen, joint venture, foreign
    directors = db.Column(db.JSON)
    shareholders = db.Column(db.JSON)
    beneficial_owners = db.Column(db.JSON)

    # Contact
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20))
    physical_address = db.Column(db.Text)

    # Status
    status = db.Column(db.String(50), default='pending')  # pending, verified, suspended, rejected
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Workspace
    workspace_access_granted = db.Column(db.Boolean, default=False)
    workspace_folder_id = db.Column(db.String(100))

    # Fee
    fee_paid = db.Column(db.Boolean, default=False)
    fee_amount = db.Column(db.Numeric(10, 2))
    fee_receipt = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='bidders')
    verifier = db.relationship('User', foreign_keys=[verified_by])
    submissions = db.relationship('BidSubmission', back_populates='bidder', lazy='dynamic')

    def __repr__(self):
        return f'<Bidder {self.company_name}>'
