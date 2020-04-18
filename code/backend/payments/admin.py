from django.contrib import admin

from . import models as m


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["uuid", "amount", "simplepay_transaction_id", "currency", "payment_method_type", "paid_at"]


class InlinePaymentAdmin(admin.TabularInline):
    model = m.Payment
    extra = 1


class SimplePayTransactionAdmin(admin.ModelAdmin):
    inlines = [InlinePaymentAdmin]


admin.site.register(m.Payment, PaymentAdmin)
admin.site.register(m.SimplePayTransaction, SimplePayTransactionAdmin)
