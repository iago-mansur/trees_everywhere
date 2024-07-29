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
    list_display = ['email', 'name', 'get_accounts', 'created']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'name',
                    'accounts',
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
                'accounts',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    def get_accounts(self, obj):
        return ", ".join([account.name for account in obj.accounts.all()])
    get_accounts.short_description = 'Accounts'


class AccountAdmin(admin.ModelAdmin):
    """Define the admin pages for accounts."""
    ordering = ['id']
    list_display = ['name', 'is_active', 'created']
    list_filter = ['is_active']
    search_fields = ['name']
    fieldsets = (
        (None, {'fields': ('name', 'is_active')}),
        (_('Important dates'), {'fields': ('created',)}),
    )
    readonly_fields = ['created']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Account, AccountAdmin)