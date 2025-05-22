# URL Shortener - Alicia BE Assignment - Medior

## Introduction

 
 This is a robust URL shortening service built with Django and Django REST Framework. The service provides a RESTful API for creating short URLs, managing custom aliases, and tracking URL access statistics.

### Key Features
- URL shortening with automatic alias generation
- Custom alias support
- Access tracking and statistics
- RESTful API architecture
- Docker containerization
- Comprehensive test suite


### Technical Stack
- Python
- Django & Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Parameterized Testing
- Swagger

## Project Setup & Installation

**1. Clone the Repository**
```bash
git clone https://github.com/your-org/url-shortener.git
cd url-shortener
git checkout feature/dev
```

**2. execute docker**
```bash
docker-compose up -d

docker exec -it alicia-medior-be-assignment-web-1 bash
```

**3. Project URL**

http://127.0.0.1:8001

## API Endpoints 

| Method  | Endpoint              | Description |
|---------|-----------------------|-------------|
| `POST`  | `/api/shorten/`       | Submit a long URL and receive a short URL. |
| `GET`   | `/short/<short_code>/` | Redirect to the original long URL. |
| `GET`  | `/api/stats/<short_code>/` | Retrieve stats for a short URL (e.g., access count). |
 
### 1. Create Short URL
- **Endpoint**: `/api/shorten/`
- **Method**: POST
- **Request Body**:
 ```bash
 {
    "original_url": "http://www.exmaple.com",
    "custom_alias": "test"

}
```
- **Response**

 ```bash
{
    "original_url": "http://www.exmaple.com",
    "short_alias": "test",
    "created_at": "2025-05-21T03:00:01.762571Z",
    "is_custom_url": true
}
```
### 2. Redirect to Original URL
- **Endpoint**: `/short/<short_code>/`
- **Method**: GET
- **Response**: 302 Redirect to original URL

### 3. Get URL Statistics
- **Endpoint**: `/api/stats/<short_code>`
- **Method**: GET
- **Success Response** (200 OK):
- **response**
 ```bash
    {
        "short_alias": "invalidssss",
        "original_url": "http://www.dddd.com",
        "created_at": "2025-05-21T03:00:01.762571Z",
        "access_count": 1,
        "last_accessed": "2025-05-21T03:01:41.687312Z"
    }
```

## API Document -SWAGGER

http://127.0.0.1:8001/swagger/

## Integration test

```bash
python manage.py test url_shortener.tests.test_views -v 2
```