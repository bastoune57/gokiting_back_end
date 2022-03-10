from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Location, TempLocation, BaseLocation, TimePeriod
from django.utils.translation import gettext_lazy as _

class UserAdmin(DjangoUserAdmin):

    # Register views to admin site
    admin.site.register(Location)
    admin.site.register(TempLocation)
    admin.site.register(BaseLocation)
    admin.site.register(TimePeriod)
