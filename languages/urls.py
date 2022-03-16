from django.urls import include, path
from rest_framework import routers
from . import views

""" 
Add app views to app router 
"""
router = routers.DefaultRouter()
router.register(r'languages', views.LanguageViewSet)

urlpatterns = [
    path('lan-stats/', views.StatsLanguageView.as_view(), name='statslanguage-list'),
]
