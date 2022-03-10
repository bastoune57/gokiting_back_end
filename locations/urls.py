from django.urls import include, path
from rest_framework import routers
from . import views

"""add app views to app router """
router = routers.DefaultRouter()
router.register(r'locations', views.LocationViewSet)
router.register(r'timeperiods', views.TimePeriodViewSet)
router.register(r'baselocations', views.BaseLocationViewSet)
router.register(r'templocations', views.TempLocationViewSet)

"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""
urlpatterns = [
    #path('', include(router.urls)), ---> not included because it is done at project level (multi app router)
]