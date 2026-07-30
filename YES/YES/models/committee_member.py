from app import db
from datetime import datetime
import pytz

class CommitteeMember(db.Model):
    __tablename__ = 'committee_members'

    id = db.Column(db.Integer, primary_key=True)
    committee_id = db.Column(db.Integer, db.ForeignKey('evaluation_committees.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Role
    role = db.Column(db.String(50), nullable=False)  # chair, vice_chair, member, secretary, adviser
    is_voting = db.Column(db.Boolean, default=True)

    # Skills/Expertise
    skills = db.Column(db.JSON)
    specialization = db.Column(db.String(200))

    # Declarations
    conflict_declared = db.Column(db.Boolean, default=False)
    conflict_details = db.Column(db.Text)
    confidentiality_signed = db.Column(db.Boolean, default=False)
    confidentiality_signed_at = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(50), default='active')  # active, suspended, recused, removed

    # Access
    access_granted_at = db.Column(db.DateTime)
    access_revoked_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    committee = db.relationship('EvaluationCommittee', back_populates='members')
    user = db.relationship('User', back_populates='committee_memberships')

    def __repr__(self):
        return f'<CommitteeMember {self.user_id} in {self.committee_id}>'
