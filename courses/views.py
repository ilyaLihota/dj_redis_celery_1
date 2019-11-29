from django.views.generic.list import ListView
from .models import Course


class ManageCourseListView(ListView):
    model = Course
    template_name = 'course/manage/course/list.html'

    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)