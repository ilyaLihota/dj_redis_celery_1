import logging
import redis

from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .forms import CalculateForm
from .tasks import send_email_to_me, get_factorial


# Get an instance of a logger.
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class CalculateFactorial(FormView):
    """
    Calculates a factorial of the number.
    """
    form_class = CalculateForm
    template_name = 'study/base.html'
    success_url = reverse_lazy('calculate')

    def get(self, request, *args, **kwargs):
        try:
            r.incr('page:views')
        except Exception:
            r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        logger.info('Get a page study/.')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        try:
            total_views = int(r.get('page:views'))
        except Exception:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        number = form.cleaned_data['number']
        try:
            number = int(number)
        except Exception:
            logger.error('Failed to type integer!')
            return HttpResponse('You should input a non-negative integer!')
        else:
            result = get_factorial.delay(number)
        while not result.ready():
            continue
        try:
            factorial = result.get()
            logger.info('Get a factorial.')
        except Exception:
            logger.error('Negative integer!')
            return HttpResponse('You should input a non-negative integer!')
        # Save factorial in Redis db.
        r.set('factorial:{}'.format(number), factorial)
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
        except Exception:
            logger.error('Failed to type integer!')
            context['total_views'] = r.set('page:views', 0)
        return context


class SendEmail(View):
    """
    Send email to admin with amount of page views.
    """
    def get(self, request, number):
        try:
            total_views = int(r.get('page:views'))
        except Exception:
            total_views = r.set('page:views', 0)
            logger.error('Wrong type of page:views! Set 0.')
        factorial = int(r.get('factorial:{}'.format(number)))
        send_email_to_me.delay(total_views, number, factorial)
        logger.info('Sent email with the amount of views.')
        return HttpResponse('Result sent to email!')
