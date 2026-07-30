from app import db
from datetime import datetime

class SupplierCategory(db.Model):
    __tablename__ = 'supplier_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Classification
    ppra_code_id = db.Column(db.Integer, db.ForeignKey('ppra_codes.id'))

    # Requirements
    registration_required = db.Column(db.Boolean, default=True)
    tax_clearance_required = db.Column(db.Boolean, default=True)
    beneficial_ownership_required = db.Column(db.Boolean, default=True)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SupplierCategory {self.name}>'
