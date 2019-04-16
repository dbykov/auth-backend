from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from rest_framework.request import Request

from auth_backend.user.models import User


def send_resetpassword_email(request: Request, user: User):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    email64 = urlsafe_base64_encode(force_bytes(user.email))

    url_pattern = getattr(
        settings, 'RESET_PASSWORD_URL',
        '/#/reg?uidb64={uidb64}&token={token}&email64={email64}')

    project_name = getattr(settings, 'PROJECT_NAME')
    project_email = getattr(settings, 'FROM_EMAIL')

    from_email = f'{project_name} <{project_email}>'

    subject = 'Re: Запрос на восстановление пароля'

    url = request.build_absolute_uri(
        url_pattern.format(uidb64=uidb64, token=token, email64=email64)
    )
    text_template = get_template('user/resetpassword.txt')
    html_template = get_template('user/resetpassword.html')

    context = {'full_name': user.get_full_name(),
               'hyperlink': mark_safe(url),
               "project_name": project_name}
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    mail.send_mail(
        subject, text_content, from_email, [user.email],
        fail_silently=False, html_message=html_content)


def send_successful_registration_email(request: Request, user: User):
    project_name = getattr(settings, 'PROJECT_NAME')
    project_email = getattr(settings, 'FROM_EMAIL')

    from_email = f'{project_name} <{project_email}>'

    subject = 'Re: Регистрация в системе'

    url = request.build_absolute_uri('/')
    text_template = get_template('user/successful_registration.txt')
    html_template = get_template('user/successful_registration.html')

    context = {'full_name': user.get_full_name(),
               'hyperlink': mark_safe(url)}
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    mail.send_mail(
        subject, text_content, from_email, [user.email],
        fail_silently=False, html_message=html_content)
