from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

def get_botswana_time():
    return datetime.now(pytz.timezone('Africa/Gaborone'))

# Import all models so SQLAlchemy metadata knows about every table
# Order matters: base tables first, dependent tables after
from models.user import User
from models.role import Role
from models.permission import Permission, role_permissions
from models.ppra_code import PPRACode
from models.supplier_category import SupplierCategory
from models.procurement import Procurement
from models.workspace import Workspace
from models.procurement_document import ProcurementDocument
from models.bidder import Bidder
from models.bid_submission import BidSubmission
from models.technical_envelope import TechnicalEnvelope
from models.financial_envelope import FinancialEnvelope
from models.bid_opening import BidOpening
from models.evaluation_committee import EvaluationCommittee
from models.committee_member import CommitteeMember
from models.technical_evaluation import TechnicalEvaluation
from models.financial_evaluation import FinancialEvaluation
from models.clarification import Clarification
from models.award import Award
from models.complaint import Complaint
from models.audit_log import AuditLog
from models.notification import Notification
from models.activity_log import ActivityLog
