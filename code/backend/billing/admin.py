from django.contrib import admin

from . import models as m


class BillingDetailAdmin(admin.ModelAdmin):
    list_display = [
        "appointment",
        "company_name",
        "full_address",
        "tax_number",
        "created_at",
    ]


admin.site.register(m.Bill)
admin.site.register(m.BillingDetail, BillingDetailAdmin)
