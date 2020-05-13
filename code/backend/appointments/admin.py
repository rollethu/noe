from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.dateformat import time_format
from django.templatetags.l10n import localize
from django.core.exceptions import ValidationError as DjangoValidationError
from billing import models as bm
from samples.models import Sample
from payments.models import Payment
from payments import services as payment_services
from . import models as m


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "address"]


class SeatInline(admin.StackedInline):
    model = m.Seat
    # We don't want to allow buses or bigger groups sitting in the same car
    max_num = m.MAX_SEATS_PER_APPOINTMENT

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
    list_filter = ["is_registration_completed"]


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
    extra = 1
    fields = ["sampled_at", "vial"]


class QrCodeInline(admin.TabularInline):
    model = m.QRCode
    readonly_fields = ["code"]

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentAdminInlineForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ["simplepay_transaction"]

    def clean(self):
        cleaned_data = super().clean()
        payment = self.instance

        try:
            payment_services.validate_paid_at(payment, cleaned_data)
        except ValueError as e:
            self.add_error("paid_at", e)

    def save(self, commit):
        try:
            payment_services.handle_paid_at(self.instance, self.cleaned_data)
        except ValueError:
            pass  # is already handled in `.clean()`

        return super().save(commit)


class PaymentInline(admin.StackedInline):
    model = Payment
    form = PaymentAdminInlineForm
    readonly_fields = ["amount", "product_type", "payment_method_type", "currency"]
    fieldsets = (
        (None, {"fields": (("amount", "currency", "product_type", "payment_method_type"),)}),
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
                    ("qrcode", "payment_product_type"),
                    ("appointment_location", "appointment_licence_plate", "appointment_time"),
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    ("full_name", "birth_date"),
                    ("identity_card_number", "healthcare_number", "has_doctor_referral", "doctor_name"),
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
    readonly_fields = (
        "appointment_location",
        "appointment_licence_plate",
        "appointment_time",
        "qrcode",
        "payment_product_type",
    )
    search_fields = ("qrcode__code", "full_name", "identity_card_number", "healthcare_number")
    list_filter = ("birth_date", "has_doctor_referral")
    inlines = [SampleInline, PaymentInline, QrCodeInline]
    date_hierarchy = "created_at"

    def appointment_location(self, obj=None):
        return obj.appointment.location.name

    appointment_location.short_description = _("Location")

    def appointment_licence_plate(self, obj=None):
        return obj.appointment.normalized_licence_plate

    appointment_licence_plate.short_description = _("Licence plate")

    def appointment_time(self, obj=None):
        try:
            start = localize(timezone.localtime(obj.appointment.start))
        except AttributeError:
            start = ""

        try:
            end_time = time_format(timezone.localtime(obj.appointment.end), "H:i")
        except AttributeError:
            end_time = ""

        return f"{start} - {end_time}"

    appointment_time.short_description = _("Time slot")

    def payment_product_type(self, obj=None):
        return obj.payment.get_product_type_display()


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
