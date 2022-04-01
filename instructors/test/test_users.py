from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from instructors.models import User
from instructors.serializers import UserSerializer
from languages import languages as lang
from categories.models import WATER_SPORT_CHOICES

def get_location (id):
    return {
        "city": "tcity"+str(id),
        "country": "tcountry"+str(id)
        ,
        "longitude": "9.8000",
        "latitude": "8.9000"
      }

def get_full_user (id):
    return {
        "email": "ilablfbkljerfkjbas"+str(30+id)+"@t.com",
        'first_name': 'bastien',
        'last_name': 'hamet',
        'is_instructor': False,
        'rating': 5,
        'phone': '+12125552368',
        'title': '',
        'description': '',
        "languages": [
        {
        "language": lang.LANGUAGES[0+id][0]
        },
        {
        "language": lang.LANGUAGES[1+id][0]
        }
        ],
        'categories': [
        {
        "category": WATER_SPORT_CHOICES[0+id][0]
        },
        {
        "category": WATER_SPORT_CHOICES[1+id][0]
        }
        ],
        'baselocations': [
        {
        "location": get_location(0+id)
        },
        {
        "location": get_location(1+id)
        }
        ],
        'templocations': []
        }

class TestUser(APITestCase):
    url = reverse_lazy('user-list')

    def compare_nested (self, src, dest):
        # check languages correctness
        self.assertEqual(len(src["languages"]), len(dest["languages"]))
        for i in range(len(src["languages"])):
            self.assertEqual(src["languages"][i]["language"], dest["languages"][i]["language"])
        # check categories correctness
        self.assertEqual(len(src["categories"]), len(dest["categories"]))
        for i in range(len(src["categories"])):
            self.assertEqual(src["categories"][i]["category"], dest["categories"][i]["category"])
        # check base location correctness
        self.assertEqual(len(src["baselocations"]), len(dest["baselocations"]))
        for i in range(len(src["baselocations"])):
            self.assertEqual(src["baselocations"][i]["location"]["city"], dest["baselocations"][i]["location"]["city"])
            self.assertEqual(src["baselocations"][i]["location"]["country"], dest["baselocations"][i]["location"]["country"])
            self.assertEqual(src["baselocations"][i]["location"]["longitude"], dest["baselocations"][i]["location"]["longitude"])
            self.assertEqual(src["baselocations"][i]["location"]["latitude"], dest["baselocations"][i]["location"]["latitude"])

    def put_data_test(self, input_data):
        """ Test update (PUT) using a data to be sent (nested object not verified)"""
        response = self.client.put(self.user_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)    
        res = response.json().copy()
        if 'categories' not in input_data.keys():
            response.json().pop("categories")
            input_data.pop("categories")
        if 'languages' not in input_data.keys():
            response.json().pop("languages")
            input_data.pop("languages")
        if 'baselocations' not in input_data.keys():
            response.json().pop("baselocations")
            input_data.pop("baselocations")
        if 'templocations' not in input_data.keys():
            response.json().pop("templocations")
            input_data.pop("templocations")
        self.compare_nested(input_data, res)   
        return res

    def put_field_test(self, name, value):
        """ Test update (PUT) of any direct field of user """
        get_res = self.client.get(self.user_url)
        response = self.client.put(self.user_url, data={name: value}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[name], value)
        self.compare_nested(get_res.json(),response.json()) # check nested where not modified
        return response

    def test_create(self):
        print("Test User -> create")
        # check empty
        self.assertFalse(User.objects.exists())
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
        response = self.client.post(self.url, data={'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'is_instructor': False, 'rating': 5})
        self.assertEqual(response.status_code, 201)
        # check output correctness
        user_id = response.json()['id']
        excepted = {'id': user_id, 'url': 'http://testserver/users/'+str(user_id)+'/', 'email': 'b@h.com', 'first_name': 'bastien', 'last_name': 'hamet', 'is_instructor': False, 'avatar_url': 'http://testserver/media/profile_pics/einstein_EqBibwO.jpeg', 'rating': 5, 'phone': '+12125552368', 'title': '', 'description': '', 'languages': [], 'categories': [], 'baselocations': [], 'templocations': []}
        self.assertEqual(excepted, response.json())

        # check correct creation with nested objects
        correct_full_user = get_full_user(0)
        response = self.client.post(self.url, data=correct_full_user, format='json')
        self.assertEqual(response.status_code, 201)
        self.compare_nested(correct_full_user, response.json())

    # check update 
    def test_update(self):
        print("Test User -> update")

        """create user with 2 items per nested object"""

        # check correct creation with nested objects
        correct_full_user = get_full_user(0)
        response = self.client.post(self.url, data=correct_full_user, format='json')
        self.assertEqual(response.status_code, 201)

        # save user info
        self.user_id = response.json()['id']   
        self.user_email = "put@put.com"
        self.user_url = 'http://testserver/users/'+str(self.user_id)+'/'

        # update email only
        response = self.put_field_test("email", self.user_email)
        # update first_name only
        self.put_field_test("first_name", "fnput")
        # update last_name only
        self.put_field_test("last_name", "lnput")
        # update phone only
        self.put_field_test("phone", "+12125552000")
        # update is_instructor only
        self.put_field_test("is_instructor", True)
        # # update avatar_url only
        # self.put_field_test("avatar_url", "http://testserver/media/profile_pics/einstein.jpeg")
        # update rating only
        self.put_field_test("rating", 4)
        # update title only
        self.put_field_test("title", "tput")
        # update description only
        self.put_field_test("description", "dput")
        # update all (not nested) fields
        res = self.put_data_test(input_data=get_full_user(0))
        
        """ 
        update the nested objects
        Write 2 nested items per nested object:
        - 1 new item to be added to the users nested objects (to add)
        - 1 item that was present at creation (to keep)
        - 1 item that was present at creation with a change (to update)
        Behavior: is that it should add the first, keep the second, update the third and remove all previous ones
        """
        # update all (not nested) fields
        res = self.put_data_test(input_data=get_full_user(1))
