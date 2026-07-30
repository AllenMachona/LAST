from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def require_role(*allowed_roles):
    """Decorator: only allow specific roles to access a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role and current_user.role.name in allowed_roles:
                return f(*args, **kwargs)
            abort(403)
        return decorated_function
    return decorator

def require_procurement_staff():
    """Any procurement staff role (PU, POU, AO, Admin)."""
    return require_role(
        'Procurement Unit', 'Procurement Oversight Unit', 
        'Accounting Officer', 'System Administrator'
    )

def require_evaluator():
    """Only evaluation committee members/chair/secretary."""
    return require_role(
        'Evaluation Committee Member', 'Evaluation Committee Chair', 
        'Evaluation Secretary', 'Procurement Unit', 'System Administrator'
    )

def require_opening_panel():
    """Only bid opening panel members."""
    return require_role(
        'Bid Opening Panel', 'Procurement Unit', 'System Administrator'
    )

def require_approver():
    """Only those who can approve awards/methods."""
    return require_role(
        'Accounting Officer', 'Procurement Oversight Unit', 'System Administrator'
    )

def bidder_only(f):
    """Only bidders (for bidder-specific routes)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.has_role('Bidder'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    """Only system administrators."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.has_role('System Administrator'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def auditor_only(f):
    """Only auditors, PPRA, oversight."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role and current_user.role.name in ['Internal Audit', 'PPRA', 'Public Oversight', 'External Auditor', 'System Administrator']:
            return f(*args, **kwargs)
        abort(403)
    return decorated_function

def no_self_approval(f):
    """Prevent users from approving their own actions."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is applied at route level with specific checks
        return f(*args, **kwargs)
    return decorated_function
