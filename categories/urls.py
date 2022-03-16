from django.urls import path
from rest_framework import routers
from . import views

""" 
Add app views to app router 
"""
router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)

"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""
urlpatterns = [
    path('cat-stats/', views.StatsCategoryView.as_view(), name='statscategory-list'),
]
