from django_redis_celery.celery import app
from django.conf import settings
from django.core.mail import send_mail


def cash_factorial(func):
    cash = {}
    def inner(number: int):

        if number in cash.keys():
            print('Cashed result: {}'.format(cash[number]))
            return cash[number]

        result = func(number)
        cash[number] = result
        return result
    return inner


@app.task
def send_email_to_me(amount_of_view: int, number: int, factorial: int):
    """
    Sends email to me with the amount of views.
    """
    subject = 'Page viewed {} times'.format(amount_of_view)
    message = 'Dear user, page viewed: {}!\n{}! = {}'.format(amount_of_view,
                                                             number,
                                                             factorial,)
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          ['lichota.test@gmail.com'])
    return mail_sent


@app.task
@cash_factorial
def get_factorial(number: int) -> int:
    """
    Returns the factorial of a number.
    """
    if number >= 0:
        factorial = 1

        for el in range(1, number+1):
            factorial *= el

        return factorial

    raise ValueError('Factorial is defined for non-negative integers.')
