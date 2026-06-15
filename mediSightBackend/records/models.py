from django.db import models
from accounts.models import DoctorProfile, PatientProfile

class PatientRecord(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name="record")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.patient.user.get_full_name()}"

class DoctorNote(models.Model):
    class NoteType(models.TextChoices):
        ROUTINE = "ROUTINE", "Routine"
        URGENT = "URGENT", "Urgent"
        CRITICAL = "CRITICAL", "Critical"

    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name="notes")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name="authored_notes")
    note_type = models.CharField(max_length=50, choices=NoteType.choices, default=NoteType.ROUTINE)
    note_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note_type} Note by {self.doctor.user.get_full_name()} on {self.timestamp.strftime('%Y-%m-%d')}"
