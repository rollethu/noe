from django.contrib import admin
from rest_framework.authtoken.models import Token
from . import models as m


class TokenInline(admin.TabularInline):
    model = Token


class UserAdmin(admin.ModelAdmin):
    inlines = [TokenInline]


admin.site.register(m.User, UserAdmin)
