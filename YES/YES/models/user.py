from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
import pytz

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)
    last_ip = db.Column(db.String(45))
    failed_logins = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Gaborone')), 
                          onupdate=lambda: datetime.now(pytz.timezone('Africa/Gaborone')))

    # Foreign Keys
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # Relationships - explicitly specify foreign_keys where multiple FKs exist
    role = db.relationship('Role', back_populates='users')
    procurements = db.relationship('Procurement', foreign_keys='Procurement.created_by',
                                   back_populates='created_by_user', lazy='dynamic')
    committee_memberships = db.relationship('CommitteeMember', back_populates='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', back_populates='user', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_permission(self, permission_name):
        if not self.role:
            return False
        return any(p.name == permission_name for p in self.role.permissions)

    def has_role(self, role_name):
        return self.role and self.role.name == role_name

    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.now(pytz.timezone('Africa/Gaborone')):
            return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'
