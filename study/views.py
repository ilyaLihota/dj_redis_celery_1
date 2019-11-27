import logging
import redis

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from functools import reduce

from .forms import CalculateForm
from .tasks import send_email_to_me

# Get an instance of a logger
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class CalculateFactorial(View):

    def get(self, request):

        try:
            total_views = r.incr('page:views')
        except:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')

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
            except:
                total_views = r.set('page:views', 0)
                logger.error('Wrong type of page:views! Set 0.')

            number = bound_form.cleaned_data['value']

            try:
                number = int(number)
            except:
                logger.error('Failed to type integer!')
                return HttpResponse('You should input a non-negative integer!')

            if number > 0:
                factorial = reduce(lambda x, y: x * y, range(1, number + 1))
            elif number == 0:
                factorial = 1
            else:
                logger.error('Inputed negative integer!')
                return HttpResponse('You should input a non-negative integer!')

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
        except:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')

        send_email_to_me(total_views)
        logger.info('Sent email with the amount of views.')

        return HttpResponse('Result sent to email!')
