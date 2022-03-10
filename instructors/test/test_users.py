from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from instructors.models import User
from instructors.serializers import UserSerializer

class TestUser(APITestCase):
    url = reverse_lazy('user-list')

    def test_list(self):
        ## actually already covered in test create
        print("Test User -> list")

    def test_create(self):
        print("Test User -> create")
        # check empty
        self.assertFalse(User.objects.exists())
        # check no first_name
        response = self.client.post(self.url, data={'email': 'truc@truc.com', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 400)
        # check no last_name
        response = self.client.post(self.url, data={'email': 'truc@truc.com', 'first_name': 'hamet'})
        self.assertEqual(response.status_code, 400)
        # check no email
        response = self.client.post(self.url, data={'first_name': 'truc', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 400)
        # check wrong email (no .)
        response = self.client.post(self.url, data={'email': 'truc@com','first_name': 'truc', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 400)
        # check wrong email (no @)
        response = self.client.post(self.url, data={'email': 'truc.com','first_name': 'truc', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 400)
        # check wrong phone
        response = self.client.post(self.url, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'phone': '+333'})
        self.assertEqual(response.status_code, 400)
        # check wrong is_instructor
        response = self.client.post(self.url, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'is_instructor': 'truc'})
        self.assertEqual(response.status_code, 400)
        # check correct creation
        response = self.client.post(self.url, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'is_instructor': False, 'location': 'Cabarete', 'rating': 5})
        self.assertEqual(response.status_code, 201)
        #print(response.json())
        excepted = {'id': 5, 'url': 'http://testserver/users/5/', 'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'is_instructor': False, 'avatar': 'http://testserver/media/einstein.jpeg', 'location': 'Cabarete', 'rating': 5, 'phone': '+12125552368', 'title': '', 'description': '', 'languages': [], 'categories': []}
        self.assertEqual(excepted, response.json())

    # def test_create_nested(self):
    #     print("Test User -> create")
    #     # check empty
    #     self.assertFalse(User.objects.exists())
    #     tmp = UserSerializer(data={'email': 'truc@truc.com', 'last_name': 'hamet', 'first_name': 'bastien', 'categories': [{'category': 'KB'}]})
    #     print(tmp.is_valid())
    #     print(tmp.errors)
    #     print(tmp._errors)
    #     response = self.client.post(self.url, data={'email': '1@truc.com', 'last_name': 'hamet', 'first_name': 'bastien', 'categories': [{'category': 'KB'}]}, format='json')
    #     print (response.json())