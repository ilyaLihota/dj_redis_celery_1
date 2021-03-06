from django.urls import path
from . import views

urlpatterns = [
    path('', views.CalculateFactorial.as_view(), name='calculate'),
    path('send_email/<int:number>/', views.SendEmail.as_view(), name='send_email'),
]
