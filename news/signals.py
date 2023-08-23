from django.db.models.signals import post_save, m2m_changed, post_delete
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins
from .models import SubscribersCategory, Category, Post, User
from django.dispatch import receiver
from django.template.loader import render_to_string
from .tasks import send_news_after_post


# 4.	Добавьте приветственное письмо пользователю при регистрации в приложении.
# Подключаем декоратор receiver
@receiver(post_save, sender=SubscribersCategory)  # сигнал срабатывает при post_save у категории sender
def notify_user_subscribe(sender, instance, created, **kwargs):
    send_mail(
        subject=f'Подписка оформлена',
        message=f'Вы успешно подписались на категорию {instance.category.name_category}',
        from_email='matrixere@gmail.com',
        recipient_list=[f'{instance.subscriber.email}'],
    )


# dispatch_uid — уникальный идентификатор получателя сигнала в случаях, когда могут быть
# отправлены повторяющиеся сигналы. Дополнительную информацию см. в разделе
# Реализовать рассылку уведомлений подписчикам после создания новости.
@receiver(m2m_changed, sender=Post.category_post.through, dispatch_uid='notify_post_subscribe_signal')
def notify_post_subscribe(sender, instance, action, *args, **kwargs):
    if action == 'post_add':
        send_news_after_post.apply_async([instance.id], countdown=5)


# 2.	как только в неё добавляется новая статья,
# её краткое содержание приходит пользователю на электронную почту.
@receiver(m2m_changed, sender=Post.category_post.through)
def notify_post_subscribe(sender, instance, action, *args, **kwargs):
    if action == 'post_add':
        recipient_list = []
        for category in instance.category_post.all():
            for subscriber in category.subscribers.all():
                recipient_list.append(subscriber.email)
                recipient_list = list(set(recipient_list))
        html_content = render_to_string('mail_subscribers.html', {'post': instance})
        msg = EmailMultiAlternatives(
            subject=f'{instance.header}',
            from_email='matrixere@gmail.com',
            to=recipient_list
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(post_delete, sender=Post.category_post.through)
def notify_admins_post_canceled(sender, instance, **kwargs):
    subject = f'{instance.post} has canceled his post!'
    mail_admins(
        subject=subject,
        message=f'Canceled Post for {instance.date.strftime("%d %m %Y")}',
    )

    print(subject)
