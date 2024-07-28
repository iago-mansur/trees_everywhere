"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'primary_account']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'name',
                    'primary_account',  # Added 'primary_account'
                ),
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'primary_account',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class PrimaryAccountAdmin(admin.ModelAdmin):
    """Define the admin pages for primary accounts."""
    list_display = ['name']
    search_fields = ['name']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.PrimaryAccount, PrimaryAccountAdmin)