from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models.user import User
from models.role import Role
from utils.security import log_activity
from datetime import datetime
import pytz

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                flash('Account is disabled.', 'danger')
                return redirect(url_for('auth.login'))
            if user.is_locked():
                flash('Account is temporarily locked.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=remember)
            user.last_login = datetime.now(pytz.timezone('Africa/Gaborone'))
            user.failed_logins = 0
            db.session.commit()
            log_activity(user.id, 'login', 'User logged in')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            if user:
                user.failed_logins += 1
                if user.failed_logins >= 5:
                    from datetime import timedelta
                    user.locked_until = datetime.now(pytz.timezone('Africa/Gaborone')) + timedelta(minutes=30)
                db.session.commit()
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        bidder_role = Role.query.filter_by(name='Bidder').first()
        user = User(username=username, email=email, first_name=first_name, last_name=last_name,
                    role_id=bidder_role.id if bidder_role else None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, 'logout', 'User logged out')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.index'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
