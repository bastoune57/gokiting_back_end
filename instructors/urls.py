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
router.register(r'languages', views.LanguageViewSet)
router.register(r'categories', views.CategoryViewSet)

"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""
urlpatterns = [
    #path('', include(router.urls)), ---> not included because it is done at project level (multi app router)
    # View for categories statistics
    path('cat-stats/', views.StatsCategoryView.as_view(), name='statscategory-list'),
    path('lan-stats/', views.StatsLanguageView.as_view(), name='statslanguage-list'),
    # Django auth page
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
