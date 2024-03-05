from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import pytz
from datetime import datetime, timedelta

from app.professionals.models import ProfessionalSerializer
from app.appointments.models import Appointment, AppointmentSerializer


class AppointmentViewTestCase(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.factory = RequestFactory()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.professional_data = {
            "full_name": "Professional Full Name",
            "occupation": {"name": "Doctor"},
            "address": {
                "street": "Prefessional Street",
                "number": "s/n",
                "neighborhood": "Professional Neighborhood",
                "zipcode": "04040041",
                "city": "São Paulo",
                "state": "São Paulo",
                "country": "Brazil",
            },
            "contact": {
                "mobile_number": "5511940304030",
                "comercial_number": "551140304030",
                "email": "professional@email.com",
            },
        }

        self.professional = self.create_professional()

        self.appointment_data = {
            "scheduled_date": datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
            + timedelta(hours=2),
            "professional": self.professional.id,
        }

        self.appointment = self.create_appointment()

    def create_professional(self):
        professional = ProfessionalSerializer(data=self.professional_data)
        if professional.is_valid():
            return professional.save()
        return None

    def create_appointment(self):
        appointment = AppointmentSerializer(data=self.appointment_data)
        if appointment.is_valid():
            return appointment.save()
        return None

    def test_get_appointment(self):
        response = self.client.get(f"/appointments/{self.appointment.id}/")
        self.assertEqual(response.status_code, 200)

    def test_query_appointment(self):
        response = self.client.get(f"/appointments/?professional_id={self.professional.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_appointment_list(self):
        response = self.client.get("/appointments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_wrong_appointment(self):
        now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
        self.appointment_data.update({"scheduled_date": now - timedelta(days=1)})
        response = self.client.post("/appointments/", self.appointment_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Scheduled date must be in the future." in response.data)

    def test_post_appointment(self):
        now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
        self.appointment_data.update({"scheduled_date": now + timedelta(days=1)})
        response = self.client.post("/appointments/", self.appointment_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_put_appointment(self):
        now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
        data = {"scheduled_date": now + timedelta(days=2), "subject": "Some Subject"}

        response = self.client.put(f"/appointments/{self.appointment.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["subject"], "Some Subject")

    def test_delete_appointment(self):
        response = self.client.delete(f"/appointments/{self.appointment.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=self.appointment.id)
