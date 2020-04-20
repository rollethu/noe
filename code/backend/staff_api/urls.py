from rest_framework.routers import DefaultRouter
from . import views


class StaffRouter(DefaultRouter):
    root_view_name = "staff-api-root"
    APIRootView = views.StaffAPIRoot


staff_router = StaffRouter()
staff_router.register("appointments", views.AppointmentViewSet, basename="staff-appointment")
staff_router.register("seats", views.SeatViewSet, basename="staff-seat")
