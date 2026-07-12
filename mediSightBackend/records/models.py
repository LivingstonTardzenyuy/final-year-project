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

class Consultation(models.Model):
    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name="consultations")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name="consultations")
    facility_name = models.CharField(max_length=255, default="MediSight Clinic")
    vitals = models.CharField(max_length=255, blank=True, null=True)
    complaints = models.TextField(blank=True, null=True)
    examination = models.TextField(blank=True, null=True)
    investigations = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation on {self.timestamp.strftime('%Y-%m-%d')}"

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.CharField(max_length=20)
    is_video_consultation = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Appointment: {self.patient.user.get_full_name()} with {self.doctor.user.get_full_name()} on {self.date}"

class AIScan(models.Model):
    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name="ai_scans")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name="ai_scans")
    scan_type = models.CharField(max_length=255)
    image = models.ImageField(upload_to="ai_scans/", blank=True, null=True)
    result = models.CharField(max_length=255)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.scan_type} for {self.patient_record.patient.user.get_full_name()} - {self.result} ({self.confidence}%)"
