# Health Center Project

This repository is intended for the development of a CRUD system for medical appointments.

## Table of Contents

1. [Technologies](#technologies)
2. [Install and Run](#install-and-run)
3. [About](#about)

## Technologies

A list of technologies used within the project:

* [Python](https://www.python.org): Version 3.11
* [Django](https://www.djangoproject.com): Version 5.0.2
* [Django Rest Framework](https://www.django-rest-framework.org): Version 3.14.0
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/): Version 5.3.1
* [Psycopg](https://pypi.org/project/psycopg2/): Version 2.9.2
* [Yet another Swagger generator](https://drf-yasg.readthedocs.io/en/stable/readme.html): Version 1.21.7

## Install and Run

```bash
# Clone this repo
$ git clone git@github.com:jeniferss/HealthCenterProject.git

# Go into the repo app
$ cd HealthCenterProject
```

### Docker

```bash
# Install docker on your machine: https://www.docker.com/

# Run the app
$ docker compose up --build
```

### Windows

```bash
# Create a virtual environment
$ python -m venv venv

# Activate your virtual environment
$ venv\Scripts\activate

# Change the database config in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Run setup
$ .\setup.bat
```

### MacOS & Linux

```bash
# Create a virtual environment
python3 -m venv venv

# Activate your virtual environment
source venv/bin/activate

# Change the database config in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Run the setup script
$ sh setup.sh
```

### Server & Docs

Server will start at: `http://127.0.0.1:8000`
</br>
You can se the docs at: `http://127.0.0.1:8000/redoc/` or `http://127.0.0.1:8000/swagger/`

## About
Django is one of the most popular frameworks for web development using Python, typically recommended for monolithic applications.

It adheres to the MTV (Model-Template-View) structure, where "M" represents models responsible for database operations. Models are also responsible for their own integrity, as seen in the project through the use of the "validators" parameter, where rules developed with regex were applied to ORMs before saving data to validate formats. The "save" and "update" methods have been enhanced to prevent data duplication, ensuring the provision of all necessary information.

Moving on to "V," it signifies views that handle user interaction. In Django, this interaction is typically facilitated through interfaces constructed with templates, constituting the "T" in the MTV structure.

To efficiently handle object relationships, the PostgreSQL database was chosen as database. It provides advanced features, strong support for complex queries and transactions, and efficient management of large datasets

Django also enables the construction of services using the REST format through the Django Rest Framework plugin. In the context of this project, API views were developed, representing specific endpoints that implement various HTTP methods:

- **GET:** Allows the listing of objects or retrieval of details for a specific object.
- **POST:** Involves creating a new record for a particular object.
- **PUT:** Enables the editing of information for an already existing object.
- **DELETE:** Used for deleting existing objects.

These API views, in essence, serve as endpoints with defined functionalities, providing a structured way to interact with and manipulate data through the specified HTTP methods.

Another essential aspect in APIs is ensuring secure data access. One of the widely used methods, supported by Django through the Simple JWT plugin, is the JSON Web Token (JWT). With JWT, various details about the entity accessing the information can be obtained, such as user ID, permissions, and more. To achieve this, you simply need to send the token generated through the provided username and password (already created in this project's script, refer to the .env file) as a Bearer token in the Authorization header.

Finally, tests and documentation are essential for the scalability and maintenance of a system. They enable new functionalities to be added or edited without compromising the existing ones, and they allow others to understand what the code does. In this project, the tests are executed when the server starts, and the documentation has been customized and configured through a library.

