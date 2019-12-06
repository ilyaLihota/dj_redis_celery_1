from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root),
    path('paradigms/', views.ParadigmListView.as_view(), name='paradigm-list'),
    path('languages/', views.LanguageListView.as_view(), name='language-list'),
    path('programmers/', views.ProgrammerListView.as_view(), name='programmer-list'),
    path('frameworks/', views.FrameworkListView.as_view(), name='framework-list'),
    path('paradigms/<int:pk>/', views.ParadigmDetailView.as_view(), name='paradigm-detail'),
    path('languages/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),
    path('programmers/<int:pk>/', views.ProgrammerDetailView.as_view(), name='programmer-detail'),
    path('frameworks/<int:pk>/', views.FrameworkDetailView.as_view(), name='framework-detail'),
]
