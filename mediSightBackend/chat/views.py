from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import ChatMessage
from .serializers import ChatMessageSerializer

from accounts.models import PatientProfile
from records.models import PatientRecord
from django.shortcuts import get_object_or_404

def generate_llm_response(context, query):
    """
    TODO: Plug in your finetuned open-source model (e.g. Llama/Mistral) inference code here!
    For now, this is a mock integration that echoes the context to prove the engine works.
    """
    prompt = f"System: You are an AI Clinical Assistant. Here is the patient context: {context}\nUser: {query}"
    
    # Example Mock Response
    return f"This is a placeholder response from the Context Engine. I have successfully analyzed the patient's context containing {len(context)} characters. When your model is ready, drop it in generate_llm_response()!"

class ConsultationAPI(generics.CreateAPIView):
    """
    Query the AI clinical assistant (Context Engine).
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Clinical Chat'])
    def post(self, request, *args, **kwargs):
        query = request.data.get('query', '')
        patient_id = request.data.get('patient')
        
        if not patient_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"patient": "Patient ID is required to provide context."})
            
        patient = get_object_or_404(PatientProfile, id=patient_id)
        
        # Build Context String
        context = f"Patient Info: Age/DOB={patient.date_of_birth}, Gender={patient.gender}, BloodGroup={patient.blood_group}. "
        try:
            record = PatientRecord.objects.get(patient=patient)
            recent_consultations = record.consultations.order_by('-timestamp')[:3]
            recent_scans = record.ai_scans.order_by('-timestamp')[:3]
            
            if recent_consultations.exists():
                context += "Recent Consultations: "
                for c in recent_consultations:
                    context += f"[Date: {c.timestamp.date()}, Diagnosis: {c.diagnosis}, Treatment: {c.treatment}] "
            
            if recent_scans.exists():
                context += "Recent AI Scans: "
                for s in recent_scans:
                    context += f"[Type: {s.scan_type}, Result: {s.result}, Confidence: {s.confidence}%] "
        except PatientRecord.DoesNotExist:
            context += "No additional medical records found."

        # Generate Response using our bridge function
        response_text = generate_llm_response(context, query)
        
        data = request.data.copy()
        data['response'] = response_text
        data['patient_context_snapshot'] = {"context_string": context}
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
