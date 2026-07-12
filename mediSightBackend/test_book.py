import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediSightBackend.settings')
sys.path.append('/home/kongnyuy/projects/finalYear/mediSightBackend/mediSightBackend')
django.setup()

from records.serializers import AppointmentSerializer
from accounts.models import DoctorProfile, PatientProfile

doctor = DoctorProfile.objects.first()
patient = PatientProfile.objects.first()

if not doctor or not patient:
    print("Missing doctor or patient for test")
else:
    data = {
        'doctor': doctor.id,
        'date': '2026-06-19',
        'time': '10:00 AM',
        'is_video_consultation': False,
        'note': 'Test'
    }
    
    class MockRequest:
        def __init__(self, user):
            self.user = user
            
    serializer = AppointmentSerializer(data=data, context={'request': MockRequest(patient.user)})
    if serializer.is_valid():
        print("Valid!")
        try:
            appt = serializer.save()
            print(f"Created appt {appt.id}")
        except Exception as e:
            print("Error saving:", e)
    else:
        print("Invalid!", serializer.errors)
