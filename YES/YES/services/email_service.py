from flask_mail import Message
from app import mail
from flask import current_app

def send_email(to, subject, body, html=None):
    msg = Message(subject, recipients=[to], sender=current_app.config['MAIL_DEFAULT_SENDER'])
    msg.body = body
    if html:
        msg.html = html
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
