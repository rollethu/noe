from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("pay-simplepay/", views.PayAppointmentSimplePayView.as_view()),
    path("simplepay-ipn/", views.simplepay_ipn_view),
    path("simplepay-back/", views.simplepay_back_view, name="simplepay-back"),
]
