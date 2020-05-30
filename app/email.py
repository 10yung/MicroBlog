from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print('mail sent!')


def send_email(to, subject, template, **kargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MICROBLOG_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MICROBLOG_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kargs)
    msg.html = render_template(template + '.html', **kargs)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr