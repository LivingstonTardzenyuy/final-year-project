from django.contrib import admin
from .models import PatientRecord, DoctorNote

admin.site.register(PatientRecord)
admin.site.register(DoctorNote)
