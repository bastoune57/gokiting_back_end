"""gokiting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import views
from drf_yasg import openapi

# my router patch
from .patches import routers

from instructors.urls import router as instructors_router
from locations.urls import router as locations_router
from languages.urls import router as languages_router
from categories.urls import router as categories_router

# instantiate custom router that can aggregate several ones 
router = routers.DefaultRouter()
router.extend(instructors_router) # include router from instructors app
router.extend(locations_router) # include router from locations app
router.extend(languages_router) # include router from languages app
router.extend(categories_router) # include router from categories app

docs_view = views.get_schema_view(
   openapi.Info(
      title="Gokiting API Documentation",
      default_version='v1',
      description="All Apis description for gokiting project",
      terms_of_service="None so far?",
      contact=openapi.Contact(email="info@gokiting.io"),
      license=openapi.License(name="which license? (BSD License)"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),
    # docs page
    re_path(r'^docs/$', docs_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('instructors.urls')), # include urls from instructors app
    path('', include('locations.urls')), # include urls from locations app
    path('', include('languages.urls')), # include urls from locations app
    path('', include('categories.urls')), # include urls from locations app
    path('', include(router.urls)), # add routers url
    # Django auth page
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


