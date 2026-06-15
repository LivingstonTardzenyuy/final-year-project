from django.db import models
from accounts.models import DoctorProfile, PatientProfile

class Diagnosis(models.Model):
    class DiseaseType(models.TextChoices):
        TUBERCULOSIS = "TUBERCULOSIS", "Tuberculosis"
        MALARIA = "MALARIA", "Malaria"

    class ResultSource(models.TextChoices):
        ONLINE = "ONLINE", "Online"
        OFFLINE = "OFFLINE", "Offline"

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="diagnoses")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name="scans_performed")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    disease_type = models.CharField(max_length=50, choices=DiseaseType.choices)
    model_prediction = models.CharField(max_length=255)
    confidence_score = models.FloatField()
    result_source_flag = models.CharField(max_length=50, choices=ResultSource.choices, default=ResultSource.ONLINE)
    is_critical = models.BooleanField(default=False)
    image_reference = models.ImageField(upload_to="diagnoses_images/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or self.disease_type} Scan - {self.patient.user.get_full_name()} ({self.timestamp.strftime('%Y-%m-%d')})"
