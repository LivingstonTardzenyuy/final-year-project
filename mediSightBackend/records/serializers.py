from rest_framework import serializers
from .models import PatientRecord, DoctorNote, Consultation, Appointment
from diagnostics.serializers import DiagnosisSerializer
from accounts.serializers import DoctorProfileSerializer, UserSerializer, PatientProfileSerializer
from .models import PatientRecord, DoctorNote, Consultation, Appointment, AIScan

class DoctorNoteSerializer(serializers.ModelSerializer):
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)

    class Meta:
        model = DoctorNote
        fields = '__all__'
        read_only_fields = ['timestamp', 'doctor']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'doctor_profile'):
            validated_data['doctor'] = request.user.doctor_profile
        return super().create(validated_data)

class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['timestamp', 'doctor', 'patient_record']

class AIScanSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = AIScan
        fields = '__all__'
        read_only_fields = ['timestamp', 'doctor', 'patient_record']

class PatientRecordSerializer(serializers.ModelSerializer):
    notes = DoctorNoteSerializer(many=True, read_only=True)
    consultations = ConsultationSerializer(many=True, read_only=True)
    ai_scans = AIScanSerializer(many=True, read_only=True)
    # Using source from the related_name on PatientProfile.diagnoses
    diagnoses = DiagnosisSerializer(source='patient.diagnoses', many=True, read_only=True)
    user = UserSerializer(source='patient.user', read_only=True)

    class Meta:
        model = PatientRecord
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)
    patient_details = PatientProfileSerializer(source='patient', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['patient', 'status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'patient_profile'):
            validated_data['patient'] = request.user.patient_profile
        return super().create(validated_data)
