# url_shortener/tests/run_tests.py
import os
import sys
import django
import argparse
from django.test.runner import DiscoverRunner

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def run_specific_tests(test_labels=None):
    runner = DiscoverRunner(verbosity=2)
    if test_labels:
        tests = test_labels
    else:
        tests = ['tests']
    return runner.run_tests(tests)

if __name__ == '__main__':
    test_labels = []
    if args.module:
        test_labels.append(f'tests.{args.module}')
        if args.test_class:
            test_labels[-1] += f'.{args.test_class}'
            if args.test:
                test_labels[-1] += f'.{args.test}'

    run_specific_tests(test_labels)