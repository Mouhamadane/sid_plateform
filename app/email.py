import os

from flask import render_template
from flask_mail import Message

from app import create_app
from app import mail

def send_mail(recipient, subject, template, **param):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        msg = Message(
            app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
            sender = app.config['EMAIL_SENDER'],
            recipients = [recipient]
        )
        msg.body = render_template(template + '.txt', **param)
        msg.html = render_template(template + '.html', **param)
        mail.send(msg)
