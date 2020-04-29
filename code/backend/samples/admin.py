from django.contrib import admin

from . import models as m


class SampleAdmin(admin.ModelAdmin):
    list_display = ["vial", "seat", "location", "sampled_at", "created_at"]


admin.site.register(m.Sample, SampleAdmin)
