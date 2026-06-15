from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"

    role = models.CharField(max_length=50, choices=Role.choices)
    biometric_status = models.BooleanField(default=False)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    genotype = models.CharField(max_length=10, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    current_status = models.CharField(max_length=100, blank=True, null=True)
    personal_health_information = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"
