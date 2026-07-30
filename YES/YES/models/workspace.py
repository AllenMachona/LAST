from app import db
from datetime import datetime
import pytz

class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id = db.Column(db.Integer, primary_key=True)
    procurement_id = db.Column(db.Integer, db.ForeignKey('procurements.id'), unique=True, nullable=False)
    workspace_name = db.Column(db.String(200))

    # Workspace sections (JSON for flexibility)
    sections = db.Column(db.JSON, default=lambda: {
        '01_governance': True,
        '02_bidding_package': True,
        '03_published_info': True,
        '04_bidder_communications': True,
        '05_sealed_submissions': True,
        '06_bid_opening': False,
        '07_evaluation_compliance': False,
        '08_evaluation_technical': False,
        '09_evaluation_financial': False,
        '10_award': False,
        '11_complaints': False,
        '12_contract_handover': False,
        '13_audit_archive': False
    })

    # Access control
    access_config = db.Column(db.JSON, default=dict)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')),
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Relationships
    procurement = db.relationship('Procurement', back_populates='workspace')

    def is_section_active(self, section_key):
        return self.sections.get(section_key, False)

    def activate_section(self, section_key):
        if self.sections:
            self.sections[section_key] = True

    def __repr__(self):
        return f'<Workspace {self.workspace_name}>'
