import math
import time

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(amount_of_view):
    subject = 'Page viewed'
    message = 'Dear user, page viewed: {}!'.format(amount_of_view)
    mail_sent = send_mail(subject,
                          message,
                          'admin@gmail.com',
                          ['ilya.lichota@gmail.com',])
    return mail_sent


@shared_task
def get_factorial(number: int):
    time.sleep(10)
    return math.factorial(number)