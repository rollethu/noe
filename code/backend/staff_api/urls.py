from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from . import views


class StaffRouter(DefaultRouter):
    root_view_name = "staff-api-root"
    APIRootView = views.StaffAPIRoot


staff_router = StaffRouter()
staff_router.register("appointments", views.AppointmentViewSet, basename="staff-appointment")
staff_router.register("seats", views.SeatViewSet, basename="staff-seat")
staff_router.register("payments", views.PaymentViewSet, basename="staff-payment")
staff_router.register("samples", views.SampleViewSet, basename="staff-sample")

urlpatterns = [
    re_path(r"login/", views.LoginView.as_view()),
    path("traffic-control/<licence_plate>/", views.TrafficControlView.as_view()),
    path("", include(staff_router.urls)),
]
