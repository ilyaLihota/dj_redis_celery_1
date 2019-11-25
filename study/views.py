import logging
import redis

from django.conf import settings
from django.shortcuts import render
from django.views import View

from .forms import CalculateForm
from .tasks import send_email, get_factorial


# Get an instance of a logger
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Calculate(View):
    def get(self, request):
        total_views = r.incr('page:views')
        form = CalculateForm()
        return render(request, 'study/base.html', {'form': form,
                                                   'total_views': total_views,
                                                  })

    def post(self, request):
        form = CalculateForm(request.POST)

        if form.is_valid():
            total_views = r.incr('page:views')
            number = form.cleaned_data['value']

            email = send_email.delay(total_views)
            factorial = get_factorial.delay(int(number))


            logger.info('Factorial:', factorial)
            logger.error('Email:', email)

        else:
            form = CalculateForm()

        return render(request, 'study/base.html', {'form': form})
