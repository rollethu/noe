from django.contrib import admin
from billing import models as bm
from samples.models import Sample
from payments.models import Payment
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
    list_display = [
        "uuid",
        "licence_plate",
        "start",
        "phone_number",
        "email",
        "is_registration_completed",
        "created_at",
    ]
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


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ["get_email", "created_at", "code", "verified_at"]

    def get_email(self, obj):
        return obj.appointment.email

    get_email.short_description = "Email address"
    get_email.admin_order_field = "appointment__email"


class SampleInline(admin.TabularInline):
    model = Sample
    extra = 2
    fields = ["sampled_at", "vial"]


class QrCodeInline(admin.TabularInline):
    model = m.QRCode
    readonly_fields = ["code"]

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentInline(admin.StackedInline):
    model = Payment
    exclude = ["simplepay_transaction"]
    readonly_fields = ["amount", "payment_method_type", "currency"]
    fieldsets = (
        (None, {"fields": (("amount", "currency", "payment_method_type"),)}),
        (None, {"fields": (("paid_at", "proof_number", "note"),)}),
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SeatAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("full_name", "birth_date"),
                    ("identity_card_number", "healthcare_number", "has_doctor_referral"),
                )
            },
        ),
        (None, {"fields": (("phone_number", "email"),)}),
        ("Address", {"classes": ("collapse",), "fields": (("post_code", "city"), "address_line1", "address_line2")}),
    )
    list_display = (
        "full_name",
        "birth_date",
        "full_address",
        "identity_card_number",
        "healthcare_number",
        "has_doctor_referral",
        "created_at",
    )
    search_fields = ("qrcode__code", "full_name", "identity_card_number", "healthcare_number")
    list_filter = ("birth_date", "has_doctor_referral")
    inlines = [SampleInline, PaymentInline, QrCodeInline]
    date_hierarchy = "created_at"

    def has_delete_permission(self, request, obj=None):
        return False


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ["location", "start", "end", "capacity"]
    readonly_fields = ["usage"]


class QRCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "seat", "created_at"]
    readonly_fields = ["created_at"]


admin.site.register(m.Location, LocationAdmin)
admin.site.register(m.Appointment, AppointmentAdmin)
admin.site.register(m.PhoneVerification, PhoneVerificationAdmin)
admin.site.register(m.EmailVerification, EmailVerificationAdmin)
admin.site.register(m.Seat, SeatAdmin)
admin.site.register(m.TimeSlot, TimeSlotAdmin)
admin.site.register(m.QRCode, QRCodeAdmin)
