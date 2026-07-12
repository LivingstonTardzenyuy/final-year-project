from django.urls import path
from .views import DossierAPI, NoteCreationAPI, ConsultationCreateAPIView, PatientAppointmentCreateAPIView, DoctorAppointmentListAPIView, AppointmentStatusUpdateAPIView, AIScanCreateAPIView

urlpatterns = [
    path('dossier/<int:patient_id>/', DossierAPI.as_view(), name='dossier'),
    path('dossier/me/', DossierAPI.as_view(), name='my_dossier'),
    path('notes/', NoteCreationAPI.as_view(), name='notes'),
    path('consultations/', ConsultationCreateAPIView.as_view(), name='consultations'),
    path('ai-scans/', AIScanCreateAPIView.as_view(), name='ai_scans'),
    path('appointments/book/', PatientAppointmentCreateAPIView.as_view(), name='book_appointment'),
    path('appointments/doctor/', DoctorAppointmentListAPIView.as_view(), name='doctor_appointments'),
    path('appointments/<int:pk>/status/', AppointmentStatusUpdateAPIView.as_view(), name='update_appointment_status'),
]
