# services.py
import random, string
from .models import ShortURL

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_short_url(original_url):
    short_code = generate_short_code()
    while ShortURL.objects.filter(short_code=short_code).exists():
        short_code = generate_short_code()
    return ShortURL.objects.create(original_url=original_url, short_code=short_code)
