from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from django.conf import settings
from datetime import datetime, timedelta
from .models import Declaration
from users.models import CustomUser


@shared_task
def send_mail_new_response(email, username, link, content):
    html_content = render_to_string('templates/mailing/mailing_nem_response.html',
                                    {'username': username, 'link': link, 'content': content})
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новом отклике',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(f'Письмо отправлено {email}')


@shared_task
def send_mail_accept_response(email, username, link, content):
    html_content = render_to_string('templates/mailing/mailing_accept_response.html',
                                    {'username': username, 'link': link, 'content': content})
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новом отклике',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(f'Письмо отправлено {email}')


@shared_task
def newsletter():
    """Еженедельная рассылка"""
    print(f'Start at {localtime()}')
    if datetime.isoweekday(datetime.now()) == 1:
        week = localtime() - timedelta(days=7)
        users = CustomUser.objects.all()
        users_email = []
        for user in users:
            users_email.append(user.email)
        if Declaration.objects.filter(date_create__gt=week).exists():
            posts = Declaration.objects.filter(date_create__gt=week)
            html_content = render_to_string('templates/mailing/week_letter.html', {'posts': posts, })
            msg = EmailMultiAlternatives(
                subject=f'Все публикации за прошедшую неделю',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=users_email,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('Еженедельная рассылка успешна отправлена')
        else:
            print('Новых постов нет')