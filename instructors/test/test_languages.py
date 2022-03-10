from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from instructors.models import Language

class TestLanguage(APITestCase):
    url = reverse_lazy('language-list')
    uurl = reverse_lazy('user-list')

    def test_list(self):
        print("Test Langugage -> list")
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/4/', 'language': 'fr'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/4/', 'language': 'en'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = {'count': 2, 'next': None, 'previous': None, 'results': [{'url': 'http://testserver/languages/2/', 'user_id': 4, 'user': 'http://testserver/users/4/', 'language': 'fr'}, {'url': 'http://testserver/languages/3/', 'user_id': 4, 'user': 'http://testserver/users/4/', 'language': 'en'}]}
        self.assertEqual(excepted, response.json())

    def test_create(self):
        print("Test Langugage -> create")
        # check empty
        self.assertFalse(Language.objects.exists())
        # check wrong user (non existant)
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/1/', 'language': 'en'})
        self.assertEqual(response.status_code, 400)
        # check wrong language
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/3/', 'language': 'ttttttt'})
        self.assertEqual(response.status_code, 400)
        # check correct creation
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/3/', 'language': 'en'})
        self.assertEqual(response.status_code, 201)
        excepted = {
            'url': 'http://testserver/languages/1/',
            'user_id': 3,
            'user': 'http://testserver/users/3/', 
            'language': 'en'
            }
        self.assertEqual(excepted, response.json())