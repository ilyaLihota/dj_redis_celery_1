from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root),
    path('paradigms/', views.ParadigmListView.as_view(), name='paradigm_list'),
    path('languages/', views.LanguageListView.as_view(), name='languages_list'),
    path('programmers/', views.ProgrammerListView.as_view(), name='programmers_list'),
    path('frameworks/', views.FrameworkListView.as_view(), name='frameworks_list'),
    path('paradigms/<int:pk>/', views.ParadigmDetailView.as_view()),
    path('languages/<int:pk>/', views.LanguageDetailView.as_view()),
    path('programmers/<int:pk>/', views.ProgrammerDetailView.as_view()),
    path('frameworks/<int:pk>/', views.FrameworkDetailView.as_view()),
]
