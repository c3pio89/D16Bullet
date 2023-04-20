from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reviews

@receiver(post_save, sender=Reviews)
def notify_user_post(sender, instance, created, **kwargs):
    if created:
        post_author = instance.declaration.user
        post_author.email_user(
            subject=f'Новый комментарий к вашему объявлению {instance.declaration.title}',
            message=instance.review,
        )
    post_author = instance.declaration.user
    post_author.email_user(
        subject=f'{instance.declaration.user} принял ваш комментарий',
        message=f'Комментарий: {instance.review}',
    )
