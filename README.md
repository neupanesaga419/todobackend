
# 📝 Todo App API

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Django](https://img.shields.io/badge/Django-4.0-green)
![DRF](https://img.shields.io/badge/DRF-3.13.1-red)
![Docker](https://img.shields.io/badge/Docker-Environment-blue)

This is a **Django** backend project powered by **Django Rest Framework (DRF)** and Docker. It's a **Todo App API** with JWT Authentication, including functionality to import todos via CSV and manage tasks through a RESTful API.

## 🚀 Features

- **JWT Authentication** for secure user login and token management.
- Full **CRUD** operations on Todos.
- Import todos via a **CSV file**.
- REST API built with **Django Rest Framework**.
- Fully containerized using **Docker**.

## 📦 Tech Stack

- **Backend**: Django, Django Rest Framework
- **Authentication**: JWT (JSON Web Token)
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL (Dockerized)
- **Environment**: Dockerfile, `.env` configuration

---

## 📑 Table of Contents

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [JWT Authentication](#jwt-authentication)
- [Todo Import Functionality](#todo-import-functionality)
- [License](#license)

---

## 🛠️ Getting Started

Follow these instructions to get the backend up and running on your local machine.

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:neupanesaga419/todo-backend.git
   cd todo-backend
    Set Up Environment Variables: Copy the example environment file and adjust the settings:

    bash

    cp .env.example .env

    Build and Run the Docker Containers: Run the following command to build the Docker image and start the services:

    bash

    docker-compose up --build

    Migrate the Database: Once the containers are up, run the migrations:

    bash

    docker-compose exec web python manage.py migrate

    Create a Superuser: Create an admin user for the Django admin panel:

    bash

    docker-compose exec web python manage.py createsuperuser

    Access the Application:

        API Documentation (powered by DRF’s browsable API): http://localhost:8000/api/
        Django Admin: http://localhost:8000/admin/

    ```