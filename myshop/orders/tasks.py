from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.shortcuts import get_object_or_404
from django.conf import settings


@shared_task
def order_created(order_id):
    order = get_object_or_404(Order,
                              pk=order_id)
    subject = f"Order : {order_id}"
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject=subject,
                          message=message,
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[order.email])
    return mail_sent
