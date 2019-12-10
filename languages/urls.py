from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root),

    path('paradigms/', views.ParadigmListView.as_view(), name='paradigm-list'),
    path('paradigms/create/', views.ParadigmCreateView.as_view(), name='paradigm-create'),
    path('paradigms/<int:pk>/', views.ParadigmDetailView.as_view(), name='paradigm-detail'),
    path('paradigms/<int:pk>/update/', views.ParadigmUpdateView.as_view(), name='paradigm-update'),
    path('paradigms/<int:pk>/delete/', views.ParadigmDeleteView.as_view(), name='paradigm-delete'),

    path('languages/', views.LanguageListView.as_view(), name='language-list'),
    path('languages/create/', views.LanguageCreateView.as_view(), name='language-create'),
    path('languages/<int:pk>/', views.ParadigmDetailView.as_view(), name='language-detail'),
    path('languages/<int:pk>/update/', views.LanguageUpdateView.as_view(), name='language-update'),
    path('languages/<int:pk>/delete/', views.LanguageDeleteView.as_view(), name='language-delete'),

    path('programmers/', views.ProgrammerListView.as_view(), name='programmer-list'),
    path('programmers/create/', views.ProgrammerCreateView.as_view(), name='programmer-create'),
    path('programmers/<int:pk>/', views.ProgrammerDetailView.as_view(), name='programmer-detail'),
    path('programmers/<int:pk>/update/', views.ProgrammerUpdateView.as_view(), name='programmer-update'),
    path('programmers/<int:pk>/delete/', views.ProgrammerDeleteView.as_view(), name='programmer-delete'),

    path('frameworks/', views.FrameworkListView.as_view(), name='framework-list'),
    path('frameworks/create/', views.FrameworkCreateView.as_view(), name='framework-create'),
    path('frameworks/<int:pk>/', views.FrameworkDetailView.as_view(), name='framework-detail'),
    path('frameworks/<int:pk>/update/', views.FrameworkUpdateView.as_view(), name='framework-update'),
    path('frameworks/<int:pk>/delete/', views.FrameworkDeleteView.as_view(), name='framework-delete'),
]
