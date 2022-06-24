import jwt
import urllib.parse
from smtplib import SMTPException
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(email):
    verification_token = jwt.encode(payload={'email': email, 'exp': timezone.now() + timezone.timedelta(minutes=10)},
                                    key=settings.SECRET_KEY, algorithm="HS256")
    params = {
        'verification_type': 'email',
        'verification_token': verification_token
    }
    verification_url = '%s/auth/verification/?%s' % (settings.FRONTEND_BASE_URL, urllib.parse.urlencode(params))
    subject = 'Account Verification'
    from_email = settings.NO_REPLY_EMAIL
    html_message = render_to_string('emails/auth/account_verification.html', {'verification_url': verification_url})
    text_message = 'Please click on the link to verify your email'

    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message
        )
    except SMTPException:
        print('SMTP ERROR')
