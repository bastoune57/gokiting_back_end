from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

"""
#https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username/
# because we customized the default User class we need to adapt manually its admin component
"""
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no useremail field."""
    # fields when looking/changing a User
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'is_instructor',
                                         'avatar', 'rating', 'phone', 'title', 'description')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # fields when adding a new User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2', 'first_name', 'last_name', 'is_instructor',
                     'avatar', 'rating', 'phone', 'title', 'description'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
