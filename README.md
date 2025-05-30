# URL Shortener - Alicia BE Assignment - Medior

## Introduction

Welcome to the **URL Shortener** assignment!

This project implements a **simple URL shortener API** using **Django** and **Django REST Framework (DRF)**. The application allows users to submit a long URL and receive a shortened URL. Accessing the short URL redirects users to the original URL.

---

## Scenario

This is a **miniature version of bit.ly or TinyURL** allowing users to:

1. Submit a long URL and receive a shortened version.
2. Use the short URL to redirect to the original long URL.
3. View basic statistics about URL usage (access count).

---

## Features Implemented

### Core Functionality

* **Shorten a URL**: API endpoint to generate and return a unique short URL.
* **Redirect to Original URL**: Short URLs redirect users to the original submitted URLs.
* **Input Validation**: Ensures URLs provided are valid using Django's validators.
* **Database Storage**: PostgreSQL used for storing original and shortened URLs.
* **API Design**: RESTful API endpoints implemented with DRF.
* **Statistics Tracking**: Counts accesses to each short URL using Redis caching.

### Bonus Features

* **Access Counting**: Tracks and retrieves the number of times a short URL has been accessed.
* **Custom Short Codes**: Users can specify custom short codes for their URLs.
* **Rate Limiting**: DRF throttling implemented to prevent API abuse.

---

## Project Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/url-shortener.git
cd url-shortener
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install the Requirements

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations & Start the Server

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Docker & Docker Compose Setup

To simplify deployment and running the application locally, Docker and Docker Compose have been provided:

```bash
docker compose up --build
```

* Docker Compose sets up Django, PostgreSQL, and Redis services automatically.

---

## API Endpoints

| Method | Endpoint                   | Description                                    |
| ------ | -------------------------- | ---------------------------------------------- |
| `POST` | `/api/shorten/`            | Submit a long URL and receive a short URL.     |
| `GET`  | `/short/<short_code>/`     | Redirect to the original long URL.             |
| `GET`  | `/api/stats/<short_code>/` | Retrieve stats (access count) for a short URL. |

---

## Code Quality and Validation

Ensure code quality and standards by running:

* **flake8** for style checking:

```bash
flake8 .
```

* **isort** for import sorting:

```bash
isort .
```

* **black** for code formatting:

```bash
black .
```

---

## Project Structure

```
url-shortener/
├── manage.py
├── url_shortener/
│   ├── urls.py
│   ├── settings.py
│   ├── wsgi.py
│   └── asgi.py
├── shortener/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── utils/
│   │   ├── cache_utils.py
│   │   └── shortener_utils.py
│   └── signals.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Database Schema

| Field Name     | Data Type             | Description                      |
| -------------- | --------------------- | -------------------------------- |
| `id`           | Integer (Primary Key) | Auto-generated unique identifier |
| `original_url` | URLField              | Original URL provided by user    |
| `short_code`   | CharField (Unique)    | Unique short code                |
| `created_at`   | DateTimeField         | Timestamp when URL was created   |
| `access_count` | IntegerField          | Number of times URL was accessed |

---

## Considerations for Scalability & Security

* **URL Generation**: Uses Base62 encoding to ensure uniqueness and compactness.
* **Scalability**: Redis caching for statistics; horizontally scalable design with Docker Compose.
* **Security**: Input validation and rate limiting prevent common abuse patterns and vulnerabilities.

---

## Submission

* **Fork** this repository.
* Implement your solution on a new branch.
* **Create a Pull Request (PR)** with a clear summary of your implementation.
* Be ready for a review discussion!

---

## Questions You Might Encounter

* How did you generate short URLs?
* How would you scale this app for millions of users?
* What are the security concerns in URL shorteners?

---

## Good Luck & Happy Coding!
