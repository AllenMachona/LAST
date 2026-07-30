from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models.bidder import Bidder
from utils.decorators import require_procurement_staff
from datetime import datetime
import pytz

bp = Blueprint('supplier', __name__)

@bp.route('/')
@login_required
@require_procurement_staff()
def index():
    suppliers = Bidder.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@bp.route('/<int:id>/verify', methods=['POST'])
@login_required
@require_procurement_staff()
def verify(id):
    supplier = Bidder.query.get_or_404(id)
    supplier.status = 'verified'
    supplier.verified_at = datetime.now(pytz.timezone('Africa/Gaborone'))
    db.session.commit()
    flash('Supplier verified.', 'success')
    return redirect(url_for('supplier.index'))
