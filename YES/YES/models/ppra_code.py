from app import db
from datetime import datetime

class PPRACode(db.Model):
    __tablename__ = 'ppra_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # services, supplies, consultants, works
    sub_code = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    grade = db.Column(db.String(20))

    # Eligibility
    min_turnover = db.Column(db.Numeric(15, 2))
    min_experience_years = db.Column(db.Integer)
    required_certifications = db.Column(db.JSON)

    # Effective dating
    effective_from = db.Column(db.DateTime, nullable=False)
    effective_to = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PPRACode {self.code}>'
