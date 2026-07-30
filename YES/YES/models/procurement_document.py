from app import db
from datetime import datetime
import pytz

class ProcurementDocument(db.Model):
    __tablename__ = 'procurement_documents'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # bidding_package, notice, addendum, clarification, evaluation_criteria
    title = db.Column(db.String(300), nullable=False)
    file_name = db.Column(db.String(500))
    file_path = db.Column(db.String(1000))
    file_size = db.Column(db.BigInteger)
    mime_type = db.Column(db.String(100))

    # Versioning
    version = db.Column(db.Integer, default=1)
    is_current = db.Column(db.Boolean, default=True)
    previous_version_id = db.Column(db.Integer, db.ForeignKey('procurement_documents.id'))

    # Content control
    is_mandatory_clause = db.Column(db.Boolean, default=False)
    is_editable = db.Column(db.Boolean, default=True)
    content_hash = db.Column(db.String(128))  # SHA-512 hash

    # Status
    status = db.Column(db.String(50), default='draft')  # draft, under_review, approved, issued, superseded

    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='documents')
    creator = db.relationship('User', foreign_keys=[created_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    previous_version = db.relationship('ProcurementDocument', remote_side=[id])

    def __repr__(self):
        return f'<ProcurementDocument {self.title} v{self.version}>'
