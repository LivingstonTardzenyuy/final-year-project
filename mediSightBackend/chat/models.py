from django.db import models
from accounts.models import DoctorProfile, PatientProfile

class ChatMessage(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="chat_messages")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="ai_consultations")
    patient_context_snapshot = models.JSONField(default=dict, blank=True, help_text="State of the patient at the time of query")
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat regarding {self.patient.user.get_full_name()} by {self.doctor.user.get_full_name()}"
