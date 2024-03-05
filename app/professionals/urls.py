from django.urls import path
from app.professionals.views import ProfessionalView, ProfessionalDetailView

urlpatterns = [
    path("", ProfessionalView.as_view()),
    path("<int:professional_id>/", ProfessionalDetailView.as_view()),
]
