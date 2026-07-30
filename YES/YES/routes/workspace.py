from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from models.workspace import Workspace
from models.procurement import Procurement
from models.bidder import Bidder

bp = Blueprint('workspace', __name__)

@bp.route('/<int:procurement_id>')
@login_required
def view(procurement_id):
    workspace = Workspace.query.filter_by(procurement_id=procurement_id).first_or_404()
    procurement = Procurement.query.get_or_404(procurement_id)

    # Bidders: only if they are registered for this procurement
    if current_user.has_role('Bidder'):
        bidder = Bidder.query.filter_by(procurement_id=procurement_id, contact_email=current_user.email).first()
        if not bidder:
            abort(403)

    return render_template('procurement/workspace.html', workspace=workspace, procurement=procurement)
