from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from categories.models import Category

class TestCategory(APITestCase):
    uurl = reverse_lazy('user-list')
    url = reverse_lazy('category-list')
    stat_url = 'http://testserver:8000/cat-stats/'

    def test_list(self):
        print("Test Category -> list")
        pass

    def test_create(self):
        print("Test Category -> create")
        # check empty
        self.assertFalse(Category.objects.exists())
        # check wrong user (non existant)
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'category': 'KB'})
        self.assertEqual(response.status_code, 400)
        # check wrong category
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'category': 'ttttttt'})
        self.assertEqual(response.status_code, 400)
        # check correct creations
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'category': 'KF'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'category': 'SP'})
        self.assertEqual(response.status_code, 201)
        # check duplicate
        response = self.client.post(self.url, data={'user': 'http://testserver:8000/users/1/', 'category': 'KF'})
        self.assertEqual(response.status_code, 400)
        # check stat from previous 
        response = self.client.get(self.stat_url)
        self.assertEqual(response.status_code, 200)
        expected = [{'category': 'KF', 'category_count': 1}, {'category': 'SP', 'category_count': 1}]
        self.assertEqual(expected, response.json())
