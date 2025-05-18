# URL Shortener

- Code quality & structure
- Django best practices
- API design & error handling
- Database modeling
- Security considerations
- Performance optimizations (if any)

## API Endpoints

-  `POST` | `/api/v1/shorten/`
    - Submit a long URL and receive a short URL
    - Version the endpoint
    - Auth Access (Access token?)
    - Inputs
        - original_url (Required) (string)
        - custom_alias (Optional, user defined short string)
    - Response 
        - Success (201)
            - custom URL (string)
        - Error/Failed (500 or 400)
            - error message 
    - Rate limiting and logging

-  `GET` | `/api/v1/stats/<short_code>/`
    - Retrieve stats for a short URL (e.g., access count)
    - Version the endpoint
    - Auth Access (Access token?)
    - Logging
    - Response
        - Success (200)
            - access_count
            - created_at
        - Error/Failed (500 or 400)
            - error message

-  `GET` | `/short/<short_code>/`
    - Redirect to the original long URL.
    - Public Access
    - Rate Limiting
    - Logging
    - Response
        - Success (301)
            - Redirect to original URL 
        - Error/Failed (500 or 400)
            - error message

## Models

### ShortURL  

**Fields**
- original_url: String for the full URL  
- short_alias: Unique short string
    - 8 Characters (26 lowercase + 26 uppercase + 10 digits)
- access_count: Counter for URL visits
- created_at: Timestamp of creation  
- is_active: Boolean flag for soft Delete