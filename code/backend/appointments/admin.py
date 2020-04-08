from django.contrib import admin
from billing import models as bm
from . import models as m


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "address"]


class SeatInline(admin.StackedInline):
    model = m.Seat
    # We don't want to allow buses or bigger groups sitting in the same car
    max_num = 5

    def get_extra(self, request, obj=None, **kwargs):
        extra = 3
        if obj:
            extra -= obj.seats.count()
        # it will always be between 1 and 3
        return max(1, extra)


class BillingInline(admin.StackedInline):
    model = bm.BillingDetail


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["__str__", "phone_number"]
    inlines = [
        BillingInline,
        SeatInline,
    ]


class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ["get_phone_number", "created_at", "code", "verified_at"]

    def get_phone_number(self, obj):
        return obj.appointment.phone_number

    get_phone_number.short_description = "Phone number"
    get_phone_number.admin_order_field = "appointment__phone_number"


class SeatAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "birth_date",
        "full_address",
        "has_doctor_referral",
        "paid_at",
    ]


admin.site.register(m.Location, LocationAdmin)
admin.site.register(m.Appointment, AppointmentAdmin)
admin.site.register(m.PhoneVerification, PhoneVerificationAdmin)
admin.site.register(m.Seat, SeatAdmin)
