from app import db
from datetime import datetime
import pytz

class FinancialEvaluation(db.Model):
    __tablename__ = 'financial_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('bid_submissions.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Financial data
    bid_amount = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3))
    exchange_rate = db.Column(db.Numeric(10, 6))
    amount_bwp = db.Column(db.Numeric(15, 2))

    # Arithmetic
    arithmetic_errors = db.Column(db.JSON)
    corrected_amount = db.Column(db.Numeric(15, 2))

    # Preferences
    preference_applied = db.Column(db.Boolean, default=False)
    preference_percentage = db.Column(db.Numeric(5, 2))
    preference_amount = db.Column(db.Numeric(15, 2))
    evaluated_amount = db.Column(db.Numeric(15, 2))

    # Price reasonableness
    price_reasonable = db.Column(db.Boolean)
    reasonableness_notes = db.Column(db.Text)
    market_comparison = db.Column(db.JSON)

    # Scoring
    financial_score = db.Column(db.Numeric(5, 2))
    ranking = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='financial_evaluations')
    submission = db.relationship('BidSubmission')
    evaluator = db.relationship('User', foreign_keys=[evaluator_id])

    def __repr__(self):
        return f'<FinancialEvaluation {self.id}>'
