from rest_framework import serializers
from .models import Diagnosis
from accounts.serializers import PatientProfileSerializer, DoctorProfileSerializer

class DiagnosisSerializer(serializers.ModelSerializer):
    patient_details = PatientProfileSerializer(source='patient', read_only=True)
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)

    class Meta:
        model = Diagnosis
        fields = '__all__'
        read_only_fields = ['timestamp', 'doctor']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'doctor_profile'):
            validated_data['doctor'] = request.user.doctor_profile
        return super().create(validated_data)
