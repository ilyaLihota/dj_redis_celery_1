from django_redis_celery.celery import app
from django.conf import settings
from django.core.mail import send_mail


@app.task
def send_email_to_me(amount_of_view: int):
    """
    Sends email to me with the amount of views.
    """
    subject = 'Page viewed'
    message = 'Dear user, page viewed: {}!'.format(amount_of_view)
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          ['lichota.test@gmail.com'])
    return mail_sent


@app.task
def get_factorial(number: int) -> int:
    """
    Returns the factorial of a number.
    """
    if number >= 0:
        factorial = 1

        for el in range(1, number+1):
            factorial *= el

        yield factorial

    raise ValueError('Factorial is defined for non-negative integers.')


