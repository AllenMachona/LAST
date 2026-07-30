from app import db
from datetime import datetime
import pytz

class Procurement(db.Model):
    __tablename__ = 'procurements'

    id = db.Column(db.Integer, primary_key=True)
    tender_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    procurement_method = db.Column(db.String(100), nullable=False)
    submission_method = db.Column(db.String(50), default='single_envelope')
    evaluation_method = db.Column(db.String(100))

    estimated_value = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3), default='BWP')
    funding_source = db.Column(db.String(200))
    budget_confirmed = db.Column(db.Boolean, default=False)

    ppra_code = db.Column(db.String(50))
    ppra_sub_code = db.Column(db.String(50))
    ppra_grade = db.Column(db.String(20))

    status = db.Column(db.String(50), default='draft', index=True)

    publication_date = db.Column(db.DateTime)
    closing_date = db.Column(db.DateTime, index=True)
    opening_date = db.Column(db.DateTime)
    cooling_off_end = db.Column(db.DateTime)
    validity_days = db.Column(db.Integer, default=90)

    has_lots = db.Column(db.Boolean, default=False)
    lot_count = db.Column(db.Integer, default=1)

    reservation_scheme = db.Column(db.String(100))
    preference_percentage = db.Column(db.Numeric(5, 2))
    citizen_participation_required = db.Column(db.Boolean, default=False)

    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    approval_notes = db.Column(db.Text)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')),
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships - explicitly specify foreign_keys
    created_by_user = db.relationship('User', foreign_keys=[created_by], back_populates='procurements')
    approver = db.relationship('User', foreign_keys=[approved_by])
    documents = db.relationship('ProcurementDocument', back_populates='procurement', lazy='dynamic', cascade='all, delete-orphan')
    workspace = db.relationship('Workspace', back_populates='procurement', uselist=False, cascade='all, delete-orphan')
    bidders = db.relationship('Bidder', back_populates='procurement', lazy='dynamic')
    bid_submissions = db.relationship('BidSubmission', back_populates='procurement', lazy='dynamic')
    bid_openings = db.relationship('BidOpening', back_populates='procurement', lazy='dynamic')
    committees = db.relationship('EvaluationCommittee', back_populates='procurement', lazy='dynamic')
    technical_evaluations = db.relationship('TechnicalEvaluation', back_populates='procurement', lazy='dynamic')
    financial_evaluations = db.relationship('FinancialEvaluation', back_populates='procurement', lazy='dynamic')
    clarifications = db.relationship('Clarification', back_populates='procurement', lazy='dynamic')
    awards = db.relationship('Award', back_populates='procurement', lazy='dynamic')
    complaints = db.relationship('Complaint', back_populates='procurement', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', back_populates='procurement', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='procurement', lazy='dynamic')

    def __repr__(self):
        return f'<Procurement {self.tender_number}>'

    def is_active(self):
        return self.status not in ['cancelled', 'archived', 'ready_for_contract']

    def can_submit(self):
        now = datetime.now(pytz.timezone('Africa/Gaborone'))
        return self.status == 'submission_open' and self.closing_date and now < self.closing_date
