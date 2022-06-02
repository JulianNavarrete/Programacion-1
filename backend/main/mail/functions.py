from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException


def send_mail(to, subject, template, **kwargs):
    # Mail configuration
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        # Body message creation
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        # Mail sending
        result = mailsender.send(msg)
    except SMTPException as e:
        print(str(e))
        return "Mail deliver failed"
    return True
