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
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from project_noe.views import health_check
import appointments.views
import surveys.views
import samples.views
import payments.views
import users.views
from staff_api.urls import staff_router

api_router = DefaultRouter()
api_router.register("locations", appointments.views.LocationViewSet)
api_router.register("appointments", appointments.views.AppointmentViewSet)
api_router.register("seats", appointments.views.SeatViewSet)
api_router.register("time-slots", appointments.views.TimeSlotViewSet)
api_router.register("survey-questions", surveys.views.SurveyQuestionViewSet)
api_router.register("survey-answers", surveys.views.SurveyAnswerViewSet)


api_urls = [
    path("", include(api_router.urls)),
    path("verify/email/", appointments.views.VerifyEmailView.as_view()),
    path("verify/resend-email/", appointments.views.ResendVerifyEmailView.as_view()),
    path("get-price/", payments.views.GetPriceView.as_view()),
    path("pay-appointment/", payments.views.PayAppointmentView.as_view()),
]


urlpatterns = [
    path("api/", include(api_urls)),
    path("staff-api/", include(staff_router.urls)),
    path("admin/", admin.site.urls),
    path("health/", health_check),
    # for reversing only
    path("email-megerosites/", view=lambda: None, name="verify-email"),
]
