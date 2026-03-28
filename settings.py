import os
import sys

from WMG.settings import BASE_DIR

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WMG.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
    MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'