# About Gokiting Back End

This is the back-end part delivering a REST API using Python Django framework together with a Postgresql database. The main goal of this application is to provide a REST API to base the front-end development. It is not technology dependent but the FE part is done using Vue.js. The application can be summarized in a finding/booking system for watersport instructors. For deploiment the BE is provided with a Docker configuration.  

<br>

# Requirements

The only requirement is to install [Docker](https://docs.docker.com/get-docker/).  

<br>

# Getting started

## Build and start with

```
docker-compose up --build
```

## Start without building

```
docker-compose up
```

## Configure database

Only required one the first use of the DB (or after the "pgadmin" volume in Docker is removed erasing the DB)  
```
docker exec -it server-web-1 python manage.py migrate
```

<br>

# REST API CLIENT  

## Available APIs  

### General info  

Root API -> http://127.0.0.1:8000/

It displays available some of the available APIs that are accessible. Each has a link to follow to get access to it (click on it to access).

Basics on REST API standard:  
- http://<ip_address>:<port>/api_name -> **GET** (list all objects), **POST** (add 1(or+) objects)  
- http://<ip_address>:<port>/api_name/oject_id -> **GET** (one object), **PUT** (change all fields of object), **PATCH** (change only few fields of objects)  

For example, http://127.0.0.1:8000/users/ is the access to the API of the instructors. The default behavior is to make a GET request on the address which will have the effect to "get all" from table. In order to get only one instructor, one has to add "/id" to the url for example "http://127.0.0.1:8000/users/1/".  

### Get all (List)  

GET request on api below returns all instructors list: http://127.0.0.1:8000/users/  
Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X GET http://localhost:8000/users/  
```
If does not exists -> http error 404 with json  
```json
{
    "detail": "Not found."
}  
```
Example of response (JSON format):  
```json
{  
    "count":5,
    "next":null,
    "previous":null,
    "results": [ 
    { 
        "id": 5,
        "url": "http://localhost:8000/users/5/",
        "email": "NESTED3@g.com",
        "first_name": "truc",
        "last_name": "truc",
        "is_instructor": false,
        "avatar_url": "http://localhost:8000/media/einstein.jpeg",
        "rating": 3,
        "phone": "+12125552368",
        "title": "",
        "description": "",
        "languages": [],
        "categories": [
            {
                "user": "http://localhost:8000/users/5/",
                "category": "KB"
            },
            {
                "user": "http://localhost:8000/users/5/",
                "category": "WI"
            }
        ],
        "baselocations":[],
        "templocations":[]}, 
    {
        ...
    }, 
    ...
    ]
}
```

### Get one instructor

GET request on api below returns one instructors (from uid). 
http://127.0.0.1:8000/users/id  
Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X GET http://localhost:8000/users/1 
```
If does not exists -> http error 404 with json  
```json
{
    "detail": "Not found."
}  
```
Example of response:  
```json
{
    "id": 1,
    "url": "http://localhost:8000/users/1/",
    "email": "h@g.com",
    "first_name": "truc",
    "last_name": "truc",
    "is_instructor": false,
    "avatar_url": "http://localhost:8000/media/einstein.jpeg",
    "rating": 3,
    "phone": "",
    "title": "",
    "description": "",
    "languages": [],
    "categories": [
        {
            "user": "http://localhost:8000/users/1/",
            "category": "KB"
        },
        {
            "user": "http://localhost:8000/users/1/",
            "category": "WI"
        }
    ],
    "baselocations": [],
    "templocations": []
}
```

### Add one instructor

POST request on api below. It will return the json of the instructor with all fields and values saved in the DB, the id as well  
http://127.0.0.1:8000/users
Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X POST -d '{"email":"Add@example.com", "first_name": "add", "last_name": "example"}' http://localhost:8000/users/
```
If does not exists -> http error 404 with json  
```json
{
    "detail": "Not found."
}  
```
Example of response:  
```json
{
    "id": 6,
    "url": "http://localhost:8000/users/6/",
    "email": "Add@example.com",
    "first_name": "add",
    "last_name": "example",
    "is_instructor": false,
    "avatar_url": "http://localhost:8000/media/einstein.jpeg",
    "rating": 3,
    "phone": "+12125552368",
    "title": "",
    "description": "",
    "languages": [],
    "categories": [],
    "baselocations": [],
    "templocations": []
}
```

---
**Note:**
There are some informations to know when addind users:  
- To add a new users the minimum requested field is: email.
- Email must be a valid one.  
- If specified, phone must be a valid one.  
- Some fields cannot be specified: "url", "id".  
- The following fields are not part of the users object: "languages", "categories", "baselocation", "templocation". They are **nested objects**.
- A **List** of nested objects simultaneously can be added when adding a new user. It must be using the list format even for one user.
- One can add a list of user as well as single ones.
- For now baselocations and templocations are not to be used.
---

### Add multiple instructors

Example of request for adding 2 users simultaneously (using curl):  
```
application/json" -X POST -d '[{"email":"multi5555555@g.com"}, {"email":"multi3333@g.com"}]' http://localhost:8000/users/
```  

### Modify one instructor

PUT & PATCH requests on api below. A PUT requires at least to specify **ALL** the required fields, while PATCH allows smaller changes (few fields) without specifying the required fields.
http://127.0.0.1:8000/users/id
Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X PATCH -d '{"first_name": "PATCHED"}' http://localhost:8000/users/1
```
If does not exists -> http error 404 with json  
```json
{
    "detail": "Not found."
}  
```
Example of response:  
```json
{
    "id": 6,
    "url": "http://localhost:8000/users/6/",
    "email": "Add@example.com",
    "first_name": "PATCHED",
    "last_name": "example",
    "is_instructor": false,
    "avatar_url": "http://localhost:8000/media/einstein.jpeg",
    "rating": 3,
    "phone": "+12125552368",
    "title": "",
    "description": "",
    "languages": [],
    "categories": [],
    "baselocations": [],
    "templocations": []
}
```

---
**Note:**
There are some informations to know when modifying users:  
- Nested object cannot be updated so far  
---

### Add one instructor with nested objects

Example of request (using curl):  
```json
curl -H "Content-Type: application/json" -X POST -d '
{
    "email":"NESTED5@g.com", 
    "first_name": "truc", 
    "last_name": "truc", 
    "categories": [
        {
            "category":"KB"
        },
        {
            "category":"WI"
        }], 
    "languages": [
        {
            "language": "en"
        },
        {
            "language": "fr"
        }]
}' http://localhost:8000/users/
```
Example of response:  
```json

{
    "id": 8,
    "url": "http://localhost:8000/users/8/",
    "email": "NESTED5@g.com",
    "first_name": "truc",
    "last_name": "truc",
    "is_instructor": false,
    "avatar_url": "http://localhost:8000/media/einstein.jpeg",
    "rating": 3,
    "phone": "+12125552368",
    "title": "",
    "description": "",
    "languages": [
        {
            "url": "http://localhost:8000/languages/1/",
            "user": "http://localhost:8000/users/8/",
            "language": "en"
        },
        {
            "url": "http://localhost:8000/languages/2/",
            "user": "http://localhost:8000/users/8/",
            "language": "fr"
        }
    ],
    "categories": [
        {
            "user": "http://localhost:8000/users/8/",
            "category": "KB"
        },
        {
            "user": "http://localhost:8000/users/8/",
            "category": "WI"
        }
    ],
    "baselocations": [],
    "templocations": []
}
```

## Statistics

### Categories
To get statistics for categories make a get request on: http://localhost:8000/cat-stats/  
Example Response:
```json
[
    {
        "category": "KB",
        "category_count": 7
    },
    {
        "category": "WI",
        "category_count": 5
    }
]
```

### Languages
To get statistics for languages make a get request on: http://localhost:8000/lan-stats/  
Example Response:
```json
[
    {
        "language": "aa",
        "language_count": 1
    },
    {
        "language": "en",
        "language_count": 2
    },
    {
        "language": "fr",
        "language_count": 1
    }
]
```

## Filtering

### User objects filtering

It is possible to get filtered results when getting lists of instructors. Existing filters are:  
- id  
- last_name  
- first_name  
- rating  
- language  
- asc  
- desc  

Multi filtering is also possible using the "&" symbol, for the syntax please refer to the example below. Ordering of the filters in the url does not matter. 

Asc & desc options can take as value the name of a table field. One of the following: avatar_url, categories, date_joined, description, email, first_name, id, is_instructor, languages, last_login, last_name, phone, rating, title.  

Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X GET http://localhost:8000/users/?asc=rating
```  

---
**Note:**
If both asc & desc filters are given, only asc will be applied

---

Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X GET http://localhost:8000/users/?language=en&first_name=truc
```  
Example of response (JSON format):  
```json

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "url": "http://localhost:8000/users/8/",
            "email": "NESTED5@g.com",
            "first_name": "truc",
            "last_name": "truc",
            "is_instructor": false,
            "avatar_url": "http://localhost:8000/media/https%3A/github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg",
            "rating": 3,
            "phone": "+12125552368",
            "title": "",
            "description": "",
            "languages": [
                {
                    "url": "http://localhost:8000/languages/1/",
                    "user": "http://localhost:8000/users/8/",
                    "language": "en"
                },
                {
                    "url": "http://localhost:8000/languages/2/",
                    "user": "http://localhost:8000/users/8/",
                    "language": "fr"
                }
            ],
            "categories": [
                {
                    "user": "http://localhost:8000/users/8/",
                    "category": "KB"
                },
                {
                    "user": "http://localhost:8000/users/8/",
                    "category": "WI"
                }
            ],
            "baselocations": [],
            "templocations": []
        }
    ]
}
```

## Pagination

When getting larger lists of objects, the API provides a pagination system in order to avoid sendind too large data at once (taking too long or blocking FE´s memory).  

Example of chunked data (JSON format):  
```json
{
    "count": 13,
    "next": "http://localhost:8000/users/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "id": 13,
            "url": "http://localhost:8000/users/13/",
            "email": "ttcac@bc.com",
            "first_name": "caccc",
            "last_name": "cbccc",
            "is_instructor": false,
            "avatar_url": "http://localhost:8000/media/https%3A/github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg",
            "rating": 3,
            "phone": "",
            "title": "",
            "description": "",
            "languages": [],
            "categories": [],
            "baselocations": [],
            "templocations": []
        },
        ... (8 other items)
        {
            "id": 4,
            "url": "http://localhost:8000/users/4/",
            "email": "NESTED2@g.com",
            "first_name": "truc",
            "last_name": "truc",
            "is_instructor": false,
            "avatar_url": "http://localhost:8000/media/https%3A/github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg",
            "rating": 3,
            "phone": "+12125552368",
            "title": "",
            "description": "",
            "languages": [],
            "categories": [
                {
                    "user": "http://localhost:8000/users/4/",
                    "category": "KB"
                },
                {
                    "user": "http://localhost:8000/users/4/",
                    "category": "WI"
                }
            ],
            "baselocations": [],
            "templocations": []
        }
    ]
}
```

As seen in the example above, pagination allows to give only a subset of the list of object at the time providing the total amount of objects ("count"), the link to the next and previous chunks ("previous", "next"). The **pagination by default is set to 10 objects**.  

One can specify the pagination parameters in the url with the same syntax as filtering on 2 parameters:  
- **"limit"**: defines the number of object per chunk (per page)  
- **"offset"**: defines the start index of the first object from the chunk (or page)  

Example of request (using curl):  
```
curl -H "Content-Type: application/json" -X GET http://localhost:8000/users/?limit=2&offset=10
```  

Example to get a chunk of data of 2 objects maximum starting at offset 10. It means that we get the 11th and 12th objects of the total list of 13 objects (same list as used in the previous example):  
```json
{
    "count": 13,
    "next": "http://localhost:8000/users/?limit=2&offset=12",
    "previous": "http://localhost:8000/users/?limit=2&offset=8",
    "results": [
        {
            "id": 3,
            "url": "http://localhost:8000/users/3/",
            "email": "NESTEDPOST@g.com",
            "first_name": "truc",
            "last_name": "truc",
            "is_instructor": false,
            "avatar_url": "http://localhost:8000/media/https%3A/github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg",
            "rating": 3,
            "phone": "+12125552368",
            "title": "",
            "description": "",
            "languages": [],
            "categories": [
                {
                    "user": "http://localhost:8000/users/3/",
                    "category": "KB"
                }
            ],
            "baselocations": [],
            "templocations": []
        },
        {
            "id": 2,
            "url": "http://localhost:8000/users/2/",
            "email": "35122437952@mail.me",
            "first_name": "a",
            "last_name": "a",
            "is_instructor": false,
            "avatar_url": "http://localhost:8000/media/https%3A/github.com/CMQNordic/Assets/blob/main/images/unknown-person-icon-27.jpg",
            "rating": 3,
            "phone": "+12125552368",
            "title": "",
            "description": "",
            "languages": [],
            "categories": [
                {
                    "user": "http://localhost:8000/users/2/",
                    "category": "KB"
                }
            ],
            "baselocations": [],
            "templocations": []
        }
    ]
}
```  

More infos on pagination can be found [there](https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination).  

<br>

# POSTGRESQL

## Entity Relationship Diagram (ERD)
The database diagram was made using [Lucidapp](https://lucid.app)  
[Example](https://www.databasestar.com/sample-database-movies/)

## [Depreciated] ElephantSQL

### Inspection

Get url to connect from https://api.elephantsql.com From browser Tab, navigate through tables

### Some command to remember

DROP owned BY xwiunijy

### Models update

For any changes in the DB models via the Django models class one has to migrate it to the DB server 
``` 
python manage.py makemigrations
python manage.py migrate 
```

## [Depreciated] Postgresql 
Testing is done on a new created db in order not to perturb production´s db.
As ElephantSQL does not allow it, one has to start a local postgresql server using:  
```
docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```  
Then create a "gokiting" Database in order to connect the project to. For that connect to container:  
```
docker exec -it CONTAINER_ID bash
```
Then connect to Postgresql:  
```
psql -h localhost -p 5432 -U postgres -W
```
Then create DB:  
```
CREATE DATABASE gokiting;
```
Disconnnect:  
```
\q
```
Exit container:  
```
exit
```
Do not forget to change django settings:  
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',#sqlite3',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'NAME': 'gokiting',
        'HOST': '192.168.1.12',
        'PORT': '5432',
    }
}
```

# [Future task] Deployement  
## Tuto
https://openclassrooms.com/fr/courses/4425101-deployez-une-application-django/4688335-configurez-un-espace-serveur  
## CORS 
(ALLOW ALL -> WHITELIST)
## Important info (secu and stuff)
https://12factor.net/
## Static files
dev -> https://docs.djangoproject.com/en/2.1/howto/static-files/  
prod -> https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/  
## Wagtail on Heroku
https://wagtail.org/blog/deploying-wagtail-heroku/

# DJANGO REST FRAMEWORK 
https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework/7422349-tirez-le-maximum-de-ce-cours  

# TESTING

## Run test
```
python manage.py test
```


