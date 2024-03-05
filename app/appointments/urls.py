from django.urls import path
from app.appointments.views import AppointmentView, AppointmentDetailView

urlpatterns = [
    path("", AppointmentView.as_view()),
    path("<int:appointment_id>/", AppointmentDetailView.as_view()),
]
