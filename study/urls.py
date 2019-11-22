from django.urls import path
from . import views

urlpatterns = [
    path('', views.Calculate.as_view(), name='calculate'),
]
