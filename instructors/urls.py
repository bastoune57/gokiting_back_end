from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from . import views

""" 
Add app views to app router 
"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user') # basename has to be specified because of 2 different serializers
router.register(r'groups', views.GroupViewSet)
router.register(r'categories', views.CategoryViewSet)

"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""
urlpatterns = [
    #path('', include(router.urls)), ---> not included because it is done at project level (multi app router)
    # View for categories statistics
    path('cat-stats/', views.StatsCategoryView.as_view(), name='statscategory-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
