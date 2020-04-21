from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from . import models as m


class TokenInline(admin.TabularInline):
    model = Token


class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions"]
    inlines = [TokenInline]


class GroupAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(m.User, UserAdmin)
