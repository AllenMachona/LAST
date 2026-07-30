from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.notification import Notification

bp = Blueprint('notifications', __name__)

@bp.route('/')
@login_required
def index():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@bp.route('/<int:id>/read')
@login_required
def mark_read(id):
    n = Notification.query.get_or_404(id)
    if n.user_id == current_user.id:
        n.mark_read()
    return redirect(url_for('notifications.index'))
