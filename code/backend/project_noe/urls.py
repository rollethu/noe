"""project_noe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import staff_api.urls
from staff_api.permissions import StaffApiPermissions
from project_noe.views import health_check
from project_noe.views import build_info
import appointments.views
import surveys.views
import samples.views
import payments.views
import users.views


api_router = DefaultRouter()
api_router.register("locations", appointments.views.LocationViewSet)
api_router.register("appointments", appointments.views.AppointmentViewSet)
api_router.register("seats", appointments.views.SeatViewSet)
api_router.register("time-slots", appointments.views.TimeSlotViewSet)
api_router.register("survey-questions", surveys.views.SurveyQuestionViewSet)
api_router.register("survey-answers", surveys.views.SurveyAnswerViewSet)


schema_view = get_schema_view(
    openapi.Info(title="Tesztallomas.hu API", default_version="v1",),
    public=False,
    permission_classes=([StaffApiPermissions]),
)

swagger_urls = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        login_required(schema_view.without_ui(cache_timeout=0)),
        name="schema-json",
    ),
    re_path(r"^swagger/$", login_required(schema_view.with_ui("swagger", cache_timeout=0)), name="schema-swagger-ui"),
    re_path(r"^redoc/$", login_required(schema_view.with_ui("redoc", cache_timeout=0)), name="schema-redoc"),
]

api_urls = [
    path("", include(api_router.urls)),
    path("verify/email/", appointments.views.VerifyEmailView.as_view()),
    path("verify/resend-email/", appointments.views.ResendVerifyEmailView.as_view()),
    path("get-price/", payments.views.GetPriceView.as_view()),
    path("pay-appointment/", payments.views.PayAppointmentView.as_view()),
    path("", include(swagger_urls)),
]

urlpatterns = [
    path("api/", include(api_urls)),
    path("staff-api/", include(staff_api.urls)),
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("health/a1fb4d04460143e8a80b39505974859/", build_info),
    path("qrcode/<code>/", appointments.views.QRCodeView.as_view(), name="qrcode"),
]


if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
