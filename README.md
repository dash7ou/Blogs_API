# Blogs App

Its a simple API built python using FastAPI framework and use MySQL as Database has best structure for FastAPI framework for Rest API, User can login then create, get, update and delete blogs.


## Setup API

1. create python work env

         python3 -m venv {{env_name}}

2. Active env

        source ./{{env_name}}/bin/active

3. Install dependencies

        pip install -r requirements.txt

4. Run API

        uvicorn main:app --reload


Now ur env is ready.


## Arquitetura V0

```shell
.
├── models
│   ├── models.py
│   └── __init__.py
├── repository
│   ├── auth.py
│   ├── blog.py
│   ├── user.py
│   └── __init__.py
├── router
│   ├── auth.py
│   ├── blog.py
│   ├── user.py
│   └── __init__.py
├── schemas
│   ├── schemas.py
│   └── __init__.py
├── utils
│   ├── database.py
│   ├── hashing.py
│   ├── oauth2.py
│   ├── token.py
│   └── __init__.py
├── main.py
├── README.md
├── .gitignore
└── requirements.txt
```

# API Document
After run server u can open ur browser and enter

        {{server}}/docs
