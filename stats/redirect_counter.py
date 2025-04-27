"""
Count the number of per shortcode flush the counts periodically.
"""
import threading
from collections import defaultdict

_lock = threading.Lock()
_redirect_counts = defaultdict(int)

def increment_redirect_count(shortcode):
    with _lock:
        _redirect_counts[shortcode] += 1

def flush_counts():
    with _lock:
        counts = dict(_redirect_counts)
        _redirect_counts.clear()
    return counts