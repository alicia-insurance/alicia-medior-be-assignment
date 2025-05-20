from ..models import ShortURL
import random
import string

@staticmethod
def generate_unique_alias(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        alias = ''.join(random.choices(characters, k=length))
        if not ShortURL.objects.filter(short_alias=alias).exists():
            return alias