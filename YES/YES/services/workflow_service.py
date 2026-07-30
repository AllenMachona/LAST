from app import db
from models.procurement import Procurement
from datetime import datetime
import pytz

class WorkflowService:
    VALID_TRANSITIONS = {
        'draft': ['internal_review'],
        'internal_review': ['approved_for_publication', 'draft'],
        'approved_for_publication': ['published'],
        'published': ['clarification_period', 'submission_open'],
        'clarification_period': ['submission_open'],
        'submission_open': ['closed'],
        'closed': ['technical_opening'],
        'technical_opening': ['compliance_evaluation'],
        'compliance_evaluation': ['technical_evaluation'],
        'technical_evaluation': ['technical_outcome_approved'],
        'technical_outcome_approved': ['financial_opening'],
        'financial_opening': ['financial_evaluation'],
        'financial_evaluation': ['award_pending_approval'],
        'award_pending_approval': ['award_published'],
        'award_published': ['cooling_off'],
        'cooling_off': ['ready_for_contract', 'complaint_hold'],
        'complaint_hold': ['cooling_off', 'ready_for_contract'],
        'ready_for_contract': ['archived'],
        'cancelled': ['archived']
    }

    def __init__(self, procurement):
        self.procurement = procurement

    def can_transition(self, new_status):
        return new_status in self.VALID_TRANSITIONS.get(self.procurement.status, [])

    def transition(self, new_status, user_id, reason=None):
        if not self.can_transition(new_status):
            raise ValueError(f"Invalid transition from {self.procurement.status} to {new_status}")
        old_status = self.procurement.status
        self.procurement.status = new_status
        self.procurement.updated_at = datetime.now(pytz.timezone('Africa/Gaborone'))
        db.session.commit()
        from services.audit_service import log_audit
        log_audit(user_id, 'status_change', 'Procurement', self.procurement.id,
                 self.procurement.id, reason, previous_value=old_status, new_value=new_status)
        return True
