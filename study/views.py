import logging
import redis

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import CalculateForm
from .tasks import send_email_to_me, get_factorial


# Get an instance of a logger
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class CalculateFactorial(View):
    def get(self, request):
        try:
            total_views = r.incr('page:views')
        except ValueError:
            logger.error('Wrong type of total_views!')

        form = CalculateForm()
        logger.info('Get a page study/.')

        return render(request, 'study/base.html', {'form': form,
                                                   'total_views': total_views,
                                                  })

    def post(self, request):
        bound_form = CalculateForm(request.POST)
        logger.info('Get a completed form.')

        if bound_form.is_valid():
            try:
                total_views = int(r.get('page:views'))
            except ValueError:
                logger.error('Failed to type integer!')

            number = bound_form.cleaned_data['value']

            try:
                number = int(number)
            except ValueError:
                logger.error('Failed to type integer!')
                return HttpResponse('You should input an integer!')
            else:
                result = get_factorial.delay(number)

            factorial = result.get()
            logger.info('Get a factorial and sent page with the result.')

            return render(request, 'study/base.html', {'form': bound_form,
                                                       'total_views': total_views,
                                                       'number': number,
                                                       'factorial': factorial,
                                                      })
        else:
            logger.error('Form isn''t valid.')
            form = CalculateForm()

        return render(request, 'study/base.html', {'form': form})


class SendEmail(View):
    def get(self, request):
        try:
            total_views = int(r.get('page:views'))
        except ValueError:
            logger.error('Failed to type integer!')

        send_email_to_me(total_views)
        logger.info('Sent email with the amount of views.')

        return HttpResponse('Result sent to email!')
