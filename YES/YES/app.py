import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))


def create_app(config_class=Config):

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.config.from_object(config_class)

    os.makedirs(
        app.config['UPLOAD_FOLDER'],
        exist_ok=True
    )


    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'


    # Import models
    import models


    # Register blueprints

    from routes.auth import bp as auth_bp
    from routes.dashboard import bp as dashboard_bp
    from routes.procurement import bp as procurement_bp
    from routes.bid import bp as bid_bp
    from routes.audit import bp as audit_bp
    from routes.committee import bp as committee_bp
    from routes.evaluation import bp as evaluation_bp
    from routes.award import bp as award_bp
    from routes.clarification import bp as clarification_bp
    from routes.supplier import bp as supplier_bp
    from routes.reports import bp as reports_bp
    from routes.workspace import bp as workspace_bp
    from routes.notifications import bp as notifications_bp
    from routes.complaints import bp as complaints_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    app.register_blueprint(procurement_bp, url_prefix='/procurement')
    app.register_blueprint(bid_bp, url_prefix='/bid')
    app.register_blueprint(audit_bp, url_prefix='/audit')
    app.register_blueprint(committee_bp, url_prefix='/committee')
    app.register_blueprint(evaluation_bp, url_prefix='/evaluation')
    app.register_blueprint(award_bp, url_prefix='/award')
    app.register_blueprint(clarification_bp, url_prefix='/clarification')
    app.register_blueprint(supplier_bp, url_prefix='/supplier')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(workspace_bp, url_prefix='/workspace')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(complaints_bp, url_prefix='/complaints')


    # Template filters

    from utils.date_validator import format_botswana_time

    app.jinja_env.filters['botswana_time'] = format_botswana_time



    # Create database tables and default data

    with app.app_context():

        db.create_all()

        _create_default_roles()



    # Error handlers

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403


    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404



    return app




def _create_default_roles():

    from models.role import Role
    from models.user import User


    default_roles = [

        'Accounting Officer',
        'Procurement Oversight Unit',
        'Procurement Unit',
        'User Department',
        'Evaluation Committee Chair',
        'Evaluation Committee Member',
        'Evaluation Secretary',
        'Bid Opening Panel',
        'Legal',
        'Finance',
        'ICT',
        'Risk',
        'Internal Audit',
        'Bidder',
        'PPRA',
        'Public Oversight',
        'External Auditor',
        'System Administrator'

    ]


    for role_name in default_roles:

        role = Role.query.filter_by(
            name=role_name
        ).first()


        if not role:

            role = Role(
                name=role_name,
                description=f'Default {role_name} role',
                is_system=True
            )

            db.session.add(role)


    db.session.commit()



    # ADMIN USER

    if not User.query.filter_by(username="admin").first():

        admin_role = Role.query.filter_by(
            name="System Administrator"
        ).first()


        admin = User(
            username="admin",
            email="admin@ebms.gov.bw",
            first_name="System",
            last_name="Administrator",
            role_id=admin_role.id,
            is_verified=True
        )


        admin.set_password("admin123")


        db.session.add(admin)
        db.session.commit()


        print(
            "Default admin created: username=admin password=admin123"
        )



    # PROCUREMENT USER

    if not User.query.filter_by(username="procurement").first():

        role = Role.query.filter_by(
            name="Procurement Unit"
        ).first()


        user = User(
            username="procurement",
            email="procurement@ebms.gov.bw",
            first_name="Procurement",
            last_name="Officer",
            role_id=role.id,
            is_verified=True
        )


        user.set_password("procure123")


        db.session.add(user)
        db.session.commit()


        print(
            "Default procurement created: username=procurement password=procure123"
        )



    # BIDDER USER

    if not User.query.filter_by(username="bidder").first():

        role = Role.query.filter_by(
            name="Bidder"
        ).first()


        user = User(
            username="bidder",
            email="bidder@example.com",
            first_name="Test",
            last_name="Bidder",
            role_id=role.id,
            is_verified=True
        )


        user.set_password("bidder123")


        db.session.add(user)
        db.session.commit()


        print(
            "Default bidder created: username=bidder password=bidder123"
        )