from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import get_list_or_404
from R4C.settings import EMAIL
from robots.models import Robot

from .models import Order

SUBJECT = "Информация о Вашем заказе робота %s"
MESSAGE = (
    "Добрый день! "
    "Недавно вы интересовались нашим роботом версии %s. "
    "Этот робот теперь в наличии."
    "Если вам подходит этот вариант - пожалуйста, свяжитесь с нами!"
)


@receiver(post_save, sender=Robot)
def callback_order(sender, instance, **kwargs):
    try:
        variants = get_list_or_404(
            Order.objects.filter(robot_serial=instance.serial).order_by("-id")
        )
        send_mail(
            SUBJECT % (variants[0].robot_serial),
            MESSAGE % (variants[0].robot_serial),
            EMAIL,
            [
                variants[0].customer.email,
            ],
            fail_silently=False,
        )
    except Http404:
        ...
