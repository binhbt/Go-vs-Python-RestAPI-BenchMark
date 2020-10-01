FLASK RESTFUL API BOILER-PLATE WITH JWT

- [1. Deploy](#1-deploy)
  - [1.1. Install required packages](#11-install-required-packages)
  - [Create database](#create-database)
  - [Boot up rabbitmq and start celery worker](#boot-up-rabbitmq-and-start-celery-worker)
  - [1.2. Run test](#12-run-test)
  - [1.3. Run app](#13-run-app)
  - [1.4. Run all command](#14-run-all-command)
- [2. Viewing api in swagger and trying test](#2-viewing-api-in-swagger-and-trying-test)
- [3. Test using curl](#3-test-using-curl)
  - [3.1. Logging](#31-logging)
  - [3.2. Guide about token for normal user and admin](#32-guide-about-token-for-normal-user-and-admin)
  - [3.3. Normal user](#33-normal-user)
  - [3.4. Admin user and celery task](#34-admin-user-and-celery-task)
- [4. Full description and guide](#4-full-description-and-guide)
- [5. Contributing](#5-contributing)

# 1. Deploy
## 1.1. Install required packages

`pip install -r requirements.txt`
    
## Create database

By default, this sample app using sqlite, if you want to change to postgres:

```shell
docker-compose up -d postgres
docker-compose ps
```

Change config in file [config.py](app/main/config.py)

Then run:

`make db_upgrade`

## Boot up rabbitmq and start celery worker

```shell
docker-compose up -d rabbitmq
docker-compose ps
```

## 1.2. Run test

**TODO:** run test is failed, fix this

`make tests`

## 1.3. Run app

`make run`

or 

`make run-gunicorn`

## 1.4. Run all command

`make all`

# 2. Viewing api in swagger and trying test 

http://127.0.0.1:5000/api/v1/


# 3. Test using curl

## 3.1. Logging

See log message in folder log

## 3.2. Guide about token for normal user and admin

Authorization header is in the following format:

- Key: Authorization
- Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.

## 3.3. Normal user

Create user:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/user/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"test@gmail.com\", \"username\": \"test\", \"password\": \"1234\", \"public_id\": \"1\"}"
# output
{
    "status": "success",
    "message": "Successfully registered.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NTM4MzMsImlhdCI6MTU3NjU2NzQyOCwic3ViIjoyfQ.vqunxFCKwFb5boL75jmQJC1U3dVyc9BVJ8MBGIMSTFM"
}
```

Login:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"test@gmail.com\", \"password\": \"1234\"}"
# output
{
    "status": "success",
    "message": "Successfully logged in.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NTI2OTcsImlhdCI6MTU3NjU2NjI5Miwic3ViIjoxfQ.shyR184DyHtu8j5MZmxOQtn1RG8TSzsCRRsnwLGXqd0"
}
```

Get user:

```shell
curl -X GET "http://127.0.0.1:5000/api/v1/user/5f8abe86-83dc-47d7-a7ee-2808d35124d7" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjAyMjAsImlhdCI6MTU3NjU3MzgxNSwic3ViIjo1fQ.Dz1YxY0fCAsNxrj8_KRrTgjk8T5g_DZ2-D5TjUmT9dg"
# output
{
    "email": "test@gmail.com",
    "username": "test",
    "password": null,
    "public_id": "5f8abe86-83dc-47d7-a7ee-2808d35124d7"
}
```

## 3.4. Admin user and celery task

Login:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"admin@gmail.com\", \"password\": \"admin\"}"
# output
{
    "status": "success",
    "message": "Successfully logged in.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjA5NDksImlhdCI6MTU3NjU3NDU0NCwic3ViIjowfQ.Ky4q-Uu9oG9fHtWQzyEkyFUF6qDZbBwXYh8L8uz7Ltw"
}
```

List all user:

See log file for more detail:

[app.DEBUG.log](log/app.DEBUG.log)
[celery.DEBUG.log](log/celery.DEBUG.log)

```shell
curl -X GET "http://127.0.0.1:5000/api/v1/user/" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY3NDc4NTYsImlhdCI6MTU3NjY2MTQ1MSwic3ViIjowfQ.UpLjwQDgTJor1xDPP2AxrHSo3_1Koxk2N1hYp5qPmwY"
# output
{
    "data": [
        {
            "email": "admin@gmail.com",
            "username": "admin",
            "password": null,
            "public_id": "196e9bad1d1541c9b858e35ee1e8642b"
        },
        {
            "email": "user1@gmail.com",
            "username": "user1",
            "password": null,
            "public_id": "cebd65d1af534fc19f43460e0a6871fa"
        },
        {
            "email": "user2@gmail.com",
            "username": "user2",
            "password": null,
            "public_id": "698ccc22fca04fada9f92c4ad7787b2e"
        },
        {
            "email": "user3@gmail.com",
            "username": "user3",
            "password": null,
            "public_id": "29f8652348fe4656b036328fa400031f"
        },
        {
            "email": "user4@gmail.com",
            "username": "user4",
            "password": null,
            "public_id": "c480b9afb9ba425ba3c6e476a8df330e"
        }
    ]
}
```

# 4. Full description and guide

https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

or [here](How_to_structure_a_Flask-RESTPlus_web_service_for_production_builds.pdf)


# 5. Contributing
If you want to contribute to this flask restplus boilerplate, clone the repository and just start making pull requests.

```
https://github.com/cosmic-byte/flask-restplus-boilerplate.git
```
