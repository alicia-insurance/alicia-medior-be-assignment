import hashlib
import time

def generate_sha_256_hash(url):
    """Generate a SHA-256 hash for the given URL."""
    timestamp = str(int(time.time()))
    combined_string = url + timestamp
    hash_object = hashlib.sha256(combined_string.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:6]  # Return the first 6 characters of the hash


def generate_unique_shortcode(url, db_inst):
    """
    Shorten the URL and ensure uniqueness in the database.
    Approach: If a collision occurs, append a counter to the shortcode.
    Issues: TODO
    """

    shortcode = generate_sha_256_hash(url)
    counter = 1
    while db_inst.objects.filter(short_code=shortcode).exists():
        shortcode = shortcode[:5] + str(counter)
        counter += 1
    return shortcode


