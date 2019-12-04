from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('paradigms', views.ParadigmView)
router.register('languages', views.LanguageView)
router.register('programmers', views.ProgrammerView)
router.register('frameworks', views.FrameworkView)

urlpatterns = [
    path('', include(router.urls)),
]
