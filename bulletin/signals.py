from idlelib.pyshell import HOST

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Declaration, Reviews
from django.urls import reverse_lazy
from .tasks import send_mail_new_response
from .tasks import send_mail_accept_response



@receiver(m2m_changed, sender=Declaration.response.through)
def notify_new_response(sender, instance, **kwargs):
    """отправить письмо автору поста после отклика"""
    if kwargs['action'] == "post_add":
        username = instance.user.username
        email = instance.user.email
        content = instance.title
        link = reverse_lazy('mypage')
        link = HOST + f'{link}'
        send_mail_new_response.apply_async([email, username, link, content], countdown=5)


@receiver(m2m_changed, sender=Declaration.accepted_response.through)
def notify_accept_response(sender, instance, **kwargs):
    """отправить письмо юзеру оставившего отклик"""
    if kwargs['action'] == "post_add":
        user = instance.accepted_response.all().order_by('-id')[0]
        username = user.username
        email = user.email
        content = instance.title
        link = reverse_lazy('declaration', kwargs={'pk': instance.id})
        link = HOST + f'{link}'
        send_mail_accept_response.apply_async([email, username, link, content], countdown=5)