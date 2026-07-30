from app import db
from datetime import datetime
import pytz

class TechnicalEvaluation(db.Model):
    __tablename__ = 'technical_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('bid_submissions.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Criteria
    criteria_id = db.Column(db.String(100))
    criteria_name = db.Column(db.String(300))
    weight = db.Column(db.Numeric(5, 2))
    max_score = db.Column(db.Numeric(5, 2))

    # Scoring
    score = db.Column(db.Numeric(5, 2))
    comments = db.Column(db.Text)
    evidence_references = db.Column(db.JSON)

    # Pass/Fail
    is_mandatory = db.Column(db.Boolean, default=False)
    passed = db.Column(db.Boolean)

    # Consensus
    is_consensus = db.Column(db.Boolean, default=False)
    consensus_reached = db.Column(db.Boolean)
    consensus_meeting_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')),
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='technical_evaluations')
    submission = db.relationship('BidSubmission')
    evaluator = db.relationship('User', foreign_keys=[evaluator_id])

    def __repr__(self):
        return f'<TechnicalEvaluation {self.id}>'
