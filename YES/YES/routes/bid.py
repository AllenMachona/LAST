from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from models.bid_submission import BidSubmission
from models.procurement import Procurement
from models.bidder import Bidder
from utils.file_hash import calculate_file_hash
from utils.decorators import bidder_only
import os
from datetime import datetime
import pytz

bp = Blueprint('bid', __name__)

@bp.route('/submit/<int:procurement_id>', methods=['GET', 'POST'])
@login_required
def submit(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)

    # Only bidders can submit
    if not current_user.has_role('Bidder'):
        abort(403)

    if not procurement.can_submit():
        flash('Submission is not open for this procurement.', 'danger')
        return redirect(url_for('procurement.details', id=procurement_id))

    bidder = Bidder.query.filter_by(procurement_id=procurement_id, contact_email=current_user.email).first()
    if not bidder:
        bidder = Bidder(procurement_id=procurement_id, company_name=current_user.get_full_name(),
                        contact_email=current_user.email, status='verified')
        db.session.add(bidder)
        db.session.commit()

    if request.method == 'POST':
        file = request.files.get('bid_file')
        if file:
            filename = f"{procurement_id}_{bidder.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            submission = BidSubmission(
                procurement_id=procurement_id, bidder_id=bidder.id,
                envelope_type=request.form.get('envelope_type', 'single'),
                file_name=file.filename, file_path=filepath,
                file_size=os.path.getsize(filepath), file_hash=calculate_file_hash(filepath),
                status='submitted', is_final=True,
                submitted_at=datetime.now(pytz.timezone('Africa/Gaborone')),
                receipt_number=f"REC-{procurement_id}-{bidder.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            db.session.add(submission)
            db.session.commit()
            flash(f'Bid submitted. Receipt: {submission.receipt_number}', 'success')
            return redirect(url_for('procurement.details', id=procurement_id))
    return render_template('bid/submit.html', procurement=procurement)

@bp.route('/my-bids')
@login_required
@bidder_only
def my_bids():
    bidder_ids = [b.id for b in Bidder.query.filter_by(contact_email=current_user.email).all()]
    submissions = BidSubmission.query.filter(BidSubmission.bidder_id.in_(bidder_ids)).all()
    return render_template('bid/my_bids.html', submissions=submissions)
