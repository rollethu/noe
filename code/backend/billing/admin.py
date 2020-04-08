from django.contrib import admin

from . import models as m


admin.site.register(m.Bill)
admin.site.register(m.BillingDetail)
