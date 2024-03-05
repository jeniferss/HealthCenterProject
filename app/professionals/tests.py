from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from app.professionals.models import Professional, ProfessionalSerializer


class ProfessionalViewTestCase(TestCase):
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

    def create_professional(self):
        professional = ProfessionalSerializer(data=self.professional_data)
        if professional.is_valid():
            return professional.save()
        return None

    def test_get_professional(self):
        response = self.client.get(f"/professionals/{self.professional.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["full_name"], "Professional Full Name")

    def test_get_professionals_list(self):
        response = self.client.get("/professionals/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_professional(self):
        response = self.client.post(
            "/professionals/", self.professional_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Professional with the same name, occupation, address, and contact already exists."
            in response.data
        )

    def test_put_professional(self):
        data = {"social_name": "Professional Social Name"}
        response = self.client.put(f"/professionals/{self.professional.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["social_name"], "Professional Social Name")

    def test_delete_professional(self):
        response = self.client.delete(f"/professionals/{self.professional.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Professional.DoesNotExist):
            Professional.objects.get(id=self.professional.id)
