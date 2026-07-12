from django.contrib import admin
from .models import PatientRecord, DoctorNote, Consultation, Appointment

admin.site.register(PatientRecord)
admin.site.register(DoctorNote)
admin.site.register(Consultation)
admin.site.register(Appointment)
