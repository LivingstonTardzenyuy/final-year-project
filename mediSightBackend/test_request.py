import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediSightBackend.settings')
django.setup()

client = Client()
try:
    response = client.get('/')
    print("Status:", response.status_code)
    print("Content:", response.content)
except Exception as e:
    import traceback
    traceback.print_exc()
