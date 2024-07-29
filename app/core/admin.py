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
    list_display = ['email', 'name', 'get_primary_accounts', 'created']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'name',
                    'primary_accounts',
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
        (_('Important dates'), {'fields': ('last_login', 'created')}),
    )
    readonly_fields = ['last_login', 'created']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'primary_accounts',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    def get_primary_accounts(self, obj):
        return ", ".join([account.name for account in obj.primary_accounts.all()])
    get_primary_accounts.short_description = 'Primary Accounts'


class PrimaryAccountAdmin(admin.ModelAdmin):
    """Define the admin pages for primary accounts."""
    list_display = ['name']
    search_fields = ['name']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.PrimaryAccount, PrimaryAccountAdmin)