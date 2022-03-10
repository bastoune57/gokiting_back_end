from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from instructors.models import Category

class TestCategory(APITestCase):
    url = reverse_lazy('category-list')
    uurl = reverse_lazy('user-list')

    def test_list(self):
        print("Test Category -> list")
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/2/', 'category': 'KB'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = {
            'count': 1,
            'next': None, 
            'previous': None, 
            'results': [
                {
                'url': 'http://testserver/categories/2/',
                'user': 'http://testserver/users/2/', 
                'category': 'KB'
                }]
            }
        self.assertEqual(excepted, response.json())

    def test_create(self):
        print("Test Category -> list")
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        # check empty
        self.assertFalse(Category.objects.exists())
        # check wrong user (non existant)
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/10/', 'category': 'KB'})
        self.assertEqual(response.status_code, 400)
        # check wrong category
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/1/', 'category': 'SS'})
        self.assertEqual(response.status_code, 400)
        # check correct creation
        response = self.client.post(self.url, data={'user': 'http://localhost:8000/users/1/', 'category': 'KB'})
        self.assertEqual(response.status_code, 201)
        excepted = {
            'url': 'http://testserver/categories/1/',
            'user': 'http://testserver/users/1/', 
            'category': 'KB'
            }
        self.assertEqual(excepted, response.json())