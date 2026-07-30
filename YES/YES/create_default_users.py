#!/usr/bin/env python3
"""
Create default EBMS users.
Run this after starting the app (so roles exist):
    python create_default_users.py
"""

from app import create_app, db
from models.user import User
from models.role import Role

app = create_app()

with app.app_context():
    # Ensure roles exist first
    default_roles = [
        'Accounting Officer', 'Procurement Oversight Unit', 'Procurement Unit',
        'User Department', 'Evaluation Committee Chair', 'Evaluation Committee Member',
        'Evaluation Secretary', 'Bid Opening Panel', 'Legal', 'Finance', 'ICT',
        'Risk', 'Internal Audit', 'Bidder', 'PPRA', 'Public Oversight',
        'External Auditor', 'System Administrator'
    ]

    for role_name in default_roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name, description=f'Default {role_name} role'))
    db.session.commit()
    print("[OK] Roles verified/created.")

    # Helper to create user
    def make_user(username, email, first, last, role_name, password):
        if User.query.filter_by(username=username).first():
            print(f"[SKIP] User '{username}' already exists.")
            return
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"[ERROR] Role '{role_name}' not found!")
            return
        user = User(
            username=username,
            email=email,
            first_name=first,
            last_name=last,
            role_id=role.id,
            is_verified=True,
            is_active=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"[CREATED] {username} / {password}  (Role: {role_name})")

    # Create the three default accounts
    make_user('admin', 'admin@ebms.gov.bw', 'System', 'Administrator', 'System Administrator', 'admin123')
    make_user('procurement', 'procurement@ebms.gov.bw', 'Procurement', 'Officer', 'Procurement Unit', 'procure123')
    make_user('bidder', 'bidder@example.com', 'Test', 'Bidder', 'Bidder', 'bidder123')

    print("\nDone. You can now log in with any of the accounts above.")
