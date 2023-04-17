from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Рассылка',
        'News',
        'Angry-Medic@yandex.ru',
        [user_email],
        fail_silently=False,
    )