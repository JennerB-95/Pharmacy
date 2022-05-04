from config.wsgi import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from config import settings
from core.user.models import User


def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Connected..')

        email_to = 'jeotbmc@gmail.com'
        # Construimos el mensaje simple
        mensaje = MIMEMultipart("""Este es el mensaje de las narices""")
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Tienes un correo"

        content = render_to_string('send_email.html', {'user': User.objects.get(pk=1)})
        mensaje.attach(MIMEText(content, 'html'))

        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())
        print('Mail sent successfully')
    except Exception as e:
        print('e')


send_email()
