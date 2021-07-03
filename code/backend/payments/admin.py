from django.contrib import admin

from . import models as m


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "amount",
        "currency",
        "product_type",
        "payment_method_type",
        "paid_at",
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.paid_at is not None:
            editable_fields = ["note"]
            readonly_fields = [f.name for f in obj._meta.fields if f.name not in editable_fields]
            return readonly_fields

        return []


class InlinePaymentAdmin(admin.TabularInline):
    model = m.Payment
    extra = 1


admin.site.register(m.Payment, PaymentAdmin)
