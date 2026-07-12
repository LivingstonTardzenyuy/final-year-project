from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import PatientRecord, DoctorNote, Consultation, Appointment, AIScan
from .serializers import PatientRecordSerializer, DoctorNoteSerializer, ConsultationSerializer, AppointmentSerializer, AIScanSerializer
from django.shortcuts import get_object_or_404
from accounts.models import PatientProfile

class DossierAPI(generics.RetrieveAPIView):
    """
    Retrieve the complete health dossier for a patient, including notes and diagnoses.
    """
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Records'])
    def get_object(self):
        patient_id = self.kwargs.get('patient_id')
        if patient_id:
            patient = get_object_or_404(PatientProfile, id=patient_id)
        else:
            patient = self.request.user.patient_profile
        # Ensure a record exists
        record, created = PatientRecord.objects.get_or_create(patient=patient)
        return record

class NoteCreationAPI(generics.CreateAPIView):
    """
    Add a clinical note to a patient's record.
    """
    serializer_class = DoctorNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Records'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ConsultationCreateAPIView(generics.CreateAPIView):
    """
    Add a structured clinical consultation to a patient's record.
    """
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Records'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AIScanCreateAPIView(generics.CreateAPIView):
    """
    Upload an AI Scan result to a patient's record.
    """
    serializer_class = AIScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Records'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        patient_id = self.request.data.get('patient_id')
        if not patient_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"patient_id": "This field is required."})
        patient = get_object_or_404(PatientProfile, id=patient_id)
        record, _ = PatientRecord.objects.get_or_create(patient=patient)
        
        doctor = None
        if hasattr(self.request.user, 'doctor_profile'):
            doctor = self.request.user.doctor_profile
            
        serializer.save(patient_record=record, doctor=doctor)

class PatientAppointmentCreateAPIView(generics.ListCreateAPIView):
    """
    Patient can view their appointments and create new ones.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Appointments'])
    def get_queryset(self):
        if hasattr(self.request.user, 'patient_profile'):
            return Appointment.objects.filter(patient=self.request.user.patient_profile).order_by('-date', '-time')
        return Appointment.objects.none()

    @extend_schema(tags=['Appointments'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class DoctorAppointmentListAPIView(generics.ListAPIView):
    """
    Doctor can view appointments assigned to them.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Appointments'])
    def get_queryset(self):
        if hasattr(self.request.user, 'doctor_profile'):
            return Appointment.objects.filter(doctor=self.request.user.doctor_profile).order_by('date', 'time')
        return Appointment.objects.none()

class AppointmentStatusUpdateAPIView(generics.UpdateAPIView):
    """
    Doctor can update the status of an appointment (e.g. ACCEPT / REJECT).
    """
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(tags=['Appointments'])
    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()
        # Verify the user is the doctor for this appointment
        if hasattr(request.user, 'doctor_profile') and appointment.doctor == request.user.doctor_profile:
            from rest_framework.response import Response
            from rest_framework import status
            new_status = request.data.get('status')
            if new_status in [choice[0] for choice in Appointment.Status.choices]:
                appointment.status = new_status
                appointment.save()
                return Response({"status": appointment.status}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        from rest_framework.response import Response
        from rest_framework import status
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
