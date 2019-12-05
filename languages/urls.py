from django.urls import path, include
from . import views


urlpatterns = [
    path('paradigms/', views.ParadigmListView.as_view()),
    path('languages/', views.LanguageListView.as_view()),
    path('programmers/', views.ProgrammerListView.as_view()),
    path('frameworks/', views.FrameworkListView.as_view()),
    path('paradigms/<int:pk>/', views.ParadigmDetailView.as_view()),
    path('languages/<int:pk>/', views.LanguageDetailView.as_view()),
    path('programmers/<int:pk>/', views.ProgrammerDetailView.as_view()),
    path('frameworks/<int:pk>/', views.FrameworkDetailView.as_view()),
]
