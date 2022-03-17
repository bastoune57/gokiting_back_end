from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from .models import BaseLocation, Location

class TestLocation(APITestCase):
    uurl = reverse_lazy('user-list')
    url = reverse_lazy('location-list')
    burl = reverse_lazy('baselocation-list')

    def test_list(self):
        print("Test Location -> list")
        pass

    def test_create(self):
        print("Test Location -> create")
        # check empty
        self.assertFalse(Location.objects.exists())
        # check wrong location (missing latitude)
        response = self.client.post(self.url, data={'city': 'tci', 'country': 'tco', 'longitude': '8.9'})
        self.assertEqual(response.status_code, 400)
        # check wrong location (missing longitude)
        response = self.client.post(self.url, data={'city': 'tci', 'country': 'tco', 'latitude': '8.9'})
        self.assertEqual(response.status_code, 400)
        # check wrong location (missing country)
        response = self.client.post(self.url, data={'city': 'tci', 'latitude': '8.9', 'longitude': '8.9'})
        self.assertEqual(response.status_code, 400)
        # check wrong location (missing city)
        response = self.client.post(self.url, data={'latitude': '8.9', 'country': 'tco', 'longitude': '8.9'})
        self.assertEqual(response.status_code, 400)
        # check correct creations
        response = self.client.post(self.url, data={'city': 'tci', 'country': 'tco', 'longitude': '8.9', 'latitude': '8.9'})
        self.assertEqual(response.status_code, 201)
        # check duplicate 
        response = self.client.post(self.url, data={'city': 'tci', 'country': 'tco', 'longitude': '5.9', 'latitude': '5.9'})
        self.assertEqual(response.status_code, 400)

    def test_create_base(self):
        print("Test Base Location -> create")
        print(self.burl)
        ## base location
        # check empty
        self.assertFalse(BaseLocation.objects.exists())
        # check wrong user & location (non existant)
        response = self.client.post(self.burl, data={'user': 'http://testserver:8000/users/1/', 'location': 'http://testserver:8000/locations/1/'})
        self.assertEqual(response.status_code, 400)
        # check wrong location (non existant)
        response = self.client.post(self.burl, data={'user': 'http://testserver:8000/users/1/', 'location': 'http://testserver:8000/locations/1/'})
        self.assertEqual(response.status_code, 400)
        # add locations
        response = self.client.post(self.url, data={'city': 'tci', 'country': 'tco', 'longitude': '8.9', 'latitude': '8.9'})
        self.assertEqual(response.status_code, 201)
        loc_id_1 = response.json()['url']
        response = self.client.post(self.url, data={'city': 'tci2', 'country': 'tco2', 'longitude': '8.9', 'latitude': '8.9'})
        self.assertEqual(response.status_code, 201)
        loc_id_2 = response.json()['url']
        # add users
        response = self.client.post(self.uurl, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        user_id_1 = response.json()['url']
        response = self.client.post(self.uurl, data={'email': 'bas@h.com', 'first_name': 'bastien', 'last_name': 'hamet'})
        self.assertEqual(response.status_code, 201)
        user_id_2 = response.json()['url']
        # check wrong location
        response = self.client.post(self.burl, data={'user': user_id_1, 'location': 'ttttttt'})
        self.assertEqual(response.status_code, 400)
        # check correct creations
        response = self.client.post(self.burl, data={'user': user_id_1, 'location': loc_id_1})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.burl, data={'user': user_id_1, 'location': loc_id_2})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.burl, data={'user': user_id_2, 'location': loc_id_1})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.burl, data={'user': user_id_2, 'location': loc_id_2})
        self.assertEqual(response.status_code, 201)
        # check duplicate
        response = self.client.post(self.burl, data={'user': user_id_1, 'location': loc_id_1})
        self.assertEqual(response.status_code, 400)
