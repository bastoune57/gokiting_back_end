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
from django.urls import path, include

# my router patch
from .patches import routers

from instructors.urls import router as instructors_router
from locations.urls import router as locations_router

# instantiate custom router that can aggregate several ones 
router = routers.DefaultRouter()
router.extend(instructors_router) # include router from instructors app
router.extend(locations_router) # include router from locations app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('instructors.urls')), # include urls from instructors app
    path('', include('locations.urls')), # include urls from locations app
    path('', include(router.urls)), # add routers url
]


