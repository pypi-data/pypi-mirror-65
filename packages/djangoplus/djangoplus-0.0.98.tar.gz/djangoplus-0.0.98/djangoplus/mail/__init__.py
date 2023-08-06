# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives


def send_mail(subject, message, send_to, reply_to=None, actions=()):
    from djangoplus.admin.models import Settings
    url = 'http://{}'.format(settings.HOST_NAME or 'localhost:8000')
    app_settings = Settings.default()
    context = dict()
    context['subject'] = subject
    context['project_url'] = url
    context['project_name'] = app_settings.initials
    context['project_description'] = app_settings.name
    context['project_logo'] = app_settings.logo and \
        '{}/media/{}'.format(url, app_settings.logo) or '{}/static/images/mail.png'.format(url)
    context['actions'] = actions
    context['message'] = message.replace('\n', '<br>').replace('\t', '&nbsp;'*4)
    reply_to = reply_to and [reply_to] or None
    from_email = 'Não-Responder <{}>'.format(settings.SERVER_EMAIL)
    html = loader.render_to_string('mail.html', context)

    if settings.SENDGRID_KEY and 'test' not in sys.argv:
        import sendgrid
        from sendgrid.helpers.mail import Email, Content, Mail

        sg_client = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_KEY)
        from_email = Email(settings.SERVER_EMAIL)
        to_email = Email(send_to)
        content = Content("text/html", html)
        mail = Mail(from_email, subject, to_email, content)
        if reply_to:
            mail.reply_to = Email(reply_to)
        response = sg_client.client.mail.send.post(request_body=mail.get())
        return response.status_code
    else:
        body = 'Mensagem em anexo.'
        email = EmailMultiAlternatives(subject, body, from_email, [send_to], reply_to=reply_to)
        email.attach_alternative(html, "text/html")
        return email.send()
