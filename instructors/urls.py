from rest_framework import routers
from . import views

""" 
Add app views to app router 
"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user') # basename has to be specified because of 2 different serializers
router.register(r'groups', views.GroupViewSet)

"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""
urlpatterns = []
