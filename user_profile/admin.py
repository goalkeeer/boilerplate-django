from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext as _

from user_profile.models import User, Group


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'middle_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name',
                       'groups', 'user_permissions', ),
        }),
    )


admin.site.register(User, CustomUserAdmin)

# We want to change Groups through this app admin
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)
