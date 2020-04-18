from django.contrib import admin

from . import models as m


class InlinePaymentAdmin(admin.TabularInline):
    model = m.Payment
    extra = 1


class SimplePayTransactionAdmin(admin.ModelAdmin):
    inlines = [InlinePaymentAdmin]


admin.site.register(m.Payment)
admin.site.register(m.SimplePayTransaction, SimplePayTransactionAdmin)
