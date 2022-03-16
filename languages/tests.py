from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from languages.models import Language

class TestLanguage(APITestCase):
    uurl = reverse_lazy('user-list')
    url = reverse_lazy('language-list')

    def test_list(self):
        print("Test Langugage -> list")
        pass

    def test_create(self):
        print("Test Langugage -> create")
        # check empty
        self.assertFalse(Language.objects.exists())
        # check wrong user (non existant)
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'language': 'en'})
        self.assertEqual(response.status_code, 400)
        # check wrong language
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'language': 'ttttttt'})
        self.assertEqual(response.status_code, 400)
        # check correct creation
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'language': 'en'})
        self.assertEqual(response.status_code, 201)
        # check duplicate
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'language': 'en'})
        self.assertEqual(response.status_code, 400)