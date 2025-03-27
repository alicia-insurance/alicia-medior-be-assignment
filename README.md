# URL Shortener - Alicia BE Assignment - Medior

## Project Setup & Installation

**1. Clone the Repository**
```bash
git clone https://github.com/montecb/alicia-medior-be-assignment.git
cd alicia-medior-be-assignmen
```

**2. Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

**3. Install the Requirements**
```bash
pip install -r requirements.txt
```

**4. Apply Migrations & Start the Server**
```bash
python manage.py migrate
python manage.py runserver
```
## 5. API Endpoints

Certainly! Below are the sample `curl` commands for each endpoint you can add to your README file:

### 1. **Submit a Long URL and Receive a Short URL** (`POST /api/shorten/`)

```bash
curl -X POST http://localhost:8000/api/shorten/ \
    -H "Content-Type: application/json" \
    -d '{"original_url": "https://www.google.com", "custom_code": "customcode"}'
```

- **Description**: Submit a long URL and optionally provide a custom short code. The response will return a shortened URL.
- **Expected Response**:
    ```json
    {
        "short_url": "http://localhost:8000/short/customcode"
    }
    ```

---

### 2. **Redirect to the Original Long URL** (`GET /short/<short_code>/`)

```bash
curl -X GET http://localhost:8000/short/customcode/
```

- **Description**: Redirect to the original long URL using the provided short code.
- **Expected Response**: You will be redirected to the original URL, e.g., `https://www.google.com`.

---

### 3. **Retrieve Stats for a Short URL** (`GET /api/stats/<short_code>/`)

```bash
curl -X GET http://localhost:8000/api/stats/customcode/ \
    -H "Accept: application/json"
```

- **Description**: Retrieve stats for a specific short URL, such as the access count and logs.
- **Expected Response**:
    ```json
    {
    "url_details": {
        "original_url": "https://www.google.com",
        "short_code": "customcode",
        "custom_code": "customcode",
        "visit_count": 1,
        "created_at": "2025-03-27T10:07:22.387446Z"
    },
    "access_logs": [
        {
            "ip_address": "127.0.0.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "location": null,
            "accessed_at": "2025-03-27T10:07:30.037435Z"
        }
        ]
    }
    ```

---
