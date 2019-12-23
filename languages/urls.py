from django.urls import path, include
from . import views


urlpatterns = [
    path('api/v1/', views.api_root),

    path('api/v1/paradigms/', views.ParadigmListView.as_view(), name='paradigm-list'),
    path('api/v1/paradigms/<int:pk>/', views.ParadigmDetailView.as_view(), name='paradigm-detail'),
    path('api/v1/paradigms/create/', views.ParadigmCreateView.as_view(), name='paradigm-create'),
    path('api/v1/paradigms/<int:pk>/update/', views.ParadigmUpdateView.as_view(), name='paradigm-update'),
    path('api/v1/paradigms/<int:pk>/delete/', views.ParadigmDeleteView.as_view(), name='paradigm-delete'),

    path('api/v1/languages/', views.LanguageListView.as_view(), name='language-list'),
    path('api/v1/languages/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),
    path('api/v1/languages/create/', views.LanguageCreateView.as_view(), name='language-create'),
    path('api/v1/languages/<int:pk>/update/', views.LanguageUpdateView.as_view(), name='language-update'),
    path('api/v1/languages/<int:pk>/delete/', views.LanguageDeleteView.as_view(), name='language-delete'),

    path('api/v1/programmers/', views.ProgrammerListView.as_view(), name='programmer-list'),
    path('api/v1/programmers/<int:pk>/', views.ProgrammerDetailView.as_view(), name='programmer-detail'),
    path('api/v1/programmers/create/', views.ProgrammerCreateView.as_view(), name='programmer-create'),
    path('api/v1/programmers/<int:pk>/update/', views.ProgrammerUpdateView.as_view(), name='programmer-update'),
    path('api/v1/programmers/<int:pk>/delete/', views.ProgrammerDeleteView.as_view(), name='programmer-delete'),
    path('api/v1/programmers/<int:pk>/likes/', views.ProgrammerLikesView.as_view(), name='programmer-likes'),
    path('api/v1/programmers/<int:pk>/add_like/', views.ProgrammerAddLikeView.as_view(), name='programmer-add-like'),
    path('api/v1/programmers/<int:pk>/remove_like/',
         views.ProgrammerRemoveLikeView.as_view(),
         name='programmer-remove-like'),

    path('api/v1/frameworks/', views.FrameworkListView.as_view(), name='framework-list'),
    path('api/v1/frameworks/<int:pk>/', views.FrameworkDetailView.as_view(), name='framework-detail'),
    path('api/v1/frameworks/create/', views.FrameworkCreateView.as_view(), name='framework-create'),
    path('api/v1/frameworks/<int:pk>/update/', views.FrameworkUpdateView.as_view(), name='framework-update'),
    path('api/v1/frameworks/<int:pk>/delete/', views.FrameworkDeleteView.as_view(), name='framework-delete'),
]
