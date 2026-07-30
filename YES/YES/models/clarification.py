from app import db
from datetime import datetime
import pytz

class Clarification(db.Model):
    __tablename__ = 'clarifications'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)

    # Request
    requester_type = db.Column(db.String(50), nullable=False)  # bidder, evaluator, procurement_unit
    requester_id = db.Column(db.Integer)  # User or Bidder ID
    question = db.Column(db.Text, nullable=False)
    question_reference = db.Column(db.String(100))

    # Routing
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Response
    response = db.Column(db.Text)
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    responded_at = db.Column(db.DateTime)

    # Publication
    is_public = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    anonymous = db.Column(db.Boolean, default=False)  # Don't reveal bidder identity

    # Deadline
    response_deadline = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(50), default='pending')  # pending, under_review, approved, responded, published

    # Bidder alteration check
    permits_alteration = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='clarifications')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    responder = db.relationship('User', foreign_keys=[responded_by])

    def __repr__(self):
        return f'<Clarification {self.id}>'
