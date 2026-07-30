from app import db
from datetime import datetime
import pytz

class EvaluationCommittee(db.Model):
    __tablename__ = 'evaluation_committees'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)

    # Appointment
    appointment_instrument = db.Column(db.String(500))
    appointment_date = db.Column(db.DateTime)
    appointed_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Scope
    evaluation_type = db.Column(db.String(100))  # technical, financial, combined
    scope_description = db.Column(db.Text)

    # Status
    status = db.Column(db.String(50), default='appointed')  # appointed, active, suspended, dissolved

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='committees')
    members = db.relationship('CommitteeMember', back_populates='committee', lazy='dynamic', cascade='all, delete-orphan')
    appointer = db.relationship('User', foreign_keys=[appointed_by])

    def __repr__(self):
        return f'<EvaluationCommittee {self.id}>'
