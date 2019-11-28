import logging
import redis

from django.conf import settings
from django.http import HttpResponse
from django.views import View
from functools import reduce
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CalculateForm
from .tasks import send_email_to_me


# Get an instance of a logger
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class CalculateFactorial(FormView):
    """
    Calculates a factorial of number.
    """
    form_class = CalculateForm
    template_name = 'study/base.html'
    success_url = reverse_lazy('calculate')

    def get(self, request, *args, **kwargs):
        try:
            r.incr('page:views')
        except:
            r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        logger.info('Get a page study/.')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        try:
            total_views = int(r.get('page:views'))
        except:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        number = form.cleaned_data['value']
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
        return self.render_to_response({'form': form,
                                        'total_views': total_views,
                                        'number': number,
                                        'factorial': factorial,
                                       })

    def get_context_data(self, **kwargs):
        """
        Gets context, adds total_views to context and returns it.
        """
        # Get the context from parent's view.
        context = super(CalculateFactorial, self).get_context_data(**kwargs)
        # Add to the context our data.
        try:
            context['total_views'] = int(r.get('page:views'))
        except:
            logger.error('Failed to type integer!')
            context['total_views'] = r.set('page:views', 0)
        return context


class SendEmail(View):
    """
    Send email to admin with amount of views of page.
    """
    def get(self, request):
        try:
            total_views = int(r.get('page:views'))
        except:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        send_email_to_me.delay(total_views)
        logger.info('Sent email with the amount of views.')
        return HttpResponse('Result sent to email!')
