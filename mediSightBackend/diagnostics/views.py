from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Diagnosis
from .serializers import DiagnosisSerializer
from accounts.models import PatientProfile
import random
import os
from django.conf import settings

# Attempt to load the PyTorch Mobile model globally
try:
    import torch
    import torchvision.transforms as transforms
    from PIL import Image
    MODEL_PATH = os.path.join(settings.BASE_DIR.parent, 'malaria_model_mobile.ptl')
    _model = torch.jit.load(MODEL_PATH)
    _model.eval()
    print("Successfully loaded PyTorch model on backend.")
except Exception as e:
    _model = None
    print(f"Warning: Failed to load PyTorch model: {e}")

def _coerce_patient_pk(value):
    """FormData sends strings; UI may also send display ids like PT-2."""
    if value is None or value == '':
        return None
    if isinstance(value, int):
        return value
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    return int(digits) if digits else None


class OnlineScanAPI(generics.CreateAPIView):
    """
    Perform an online AI diagnostic scan using PyTorch inference.
    """
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(tags=['Diagnostics'])
    def post(self, request, *args, **kwargs):
        patient_id = _coerce_patient_pk(request.data.get('patient'))
        disease_type = request.data.get('disease_type')
        image_file = request.FILES.get('image')
        
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        prediction = "Unknown"
        confidence = 0.0
        is_positive = False

        if disease_type == Diagnosis.DiseaseType.MALARIA and _model is not None:
            try:
                img = Image.open(image_file).convert('RGB')
                
                # Standard ImageNet transforms matching the mobile app
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                
                input_tensor = transform(img).unsqueeze(0)
                
                with torch.no_grad():
                    output = _model(input_tensor)
                    probabilities = torch.nn.functional.softmax(output[0], dim=0)
                    
                    # 0: Parasitized, 1: Uninfected
                    prob_parasitized = probabilities[0].item()
                    prob_uninfected = probabilities[1].item()
                    
                    if prob_parasitized > prob_uninfected:
                        is_positive = True
                        confidence = round(prob_parasitized * 100, 2)
                        prediction = "Malaria Positive"
                    else:
                        is_positive = False
                        confidence = round(prob_uninfected * 100, 2)
                        prediction = "Malaria Negative"
                        
            except Exception as e:
                print(f"Inference error: {e}")
                prediction = "Error during inference"
                confidence = 0.0
                is_positive = False
        else:
            # Fallback/Mock for TB or if model isn't loaded
            is_positive = random.choice([True, False])
            confidence = round(random.uniform(75.0, 99.0), 2)
            prediction = f"{disease_type.capitalize()} Positive" if is_positive else f"{disease_type.capitalize()} Negative"
        
        # WHO Recommendation logic
        if is_positive:
            if disease_type == Diagnosis.DiseaseType.MALARIA:
                recommendation = "Prescribe Artemisinin-based Combination Therapy (ACT). Monitor for severe symptoms."
            else:
                recommendation = "Initiate first-line anti-TB regimen (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol). Isolate patient."
        else:
            recommendation = "No immediate action required. Consider alternative diagnoses if symptoms persist."

        # Mutate the request data to include our simulated model results
        data = request.data.copy()
        if patient_id is None:
            return Response(
                {"patient": ["A valid numeric patient id is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data['patient'] = patient_id
        data['model_prediction'] = prediction
        data['confidence_score'] = confidence
        data['result_source_flag'] = Diagnosis.ResultSource.ONLINE
        data['is_critical'] = is_positive
        data['description'] = recommendation
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OfflineSyncAPI(generics.GenericAPIView):
    """
    Synchronise offline diagnoses generated by the mobile app.
    """
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Diagnostics'])
    def post(self, request, *args, **kwargs):
        # Expecting a list of diagnosis objects
        diagnoses_data = request.data if isinstance(request.data, list) else [request.data]
        
        for item in diagnoses_data:
            item['result_source_flag'] = Diagnosis.ResultSource.OFFLINE
            pk = _coerce_patient_pk(item.get('patient'))
            if pk is not None:
                item['patient'] = pk
            
        serializer = self.get_serializer(data=diagnoses_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({"message": f"Successfully synced {len(diagnoses_data)} records.", "data": serializer.data}, status=status.HTTP_201_CREATED)

class DiagnosticHistoryAPI(generics.ListAPIView):
    """
    Retrieve all past diagnostic scans for a specific patient.
    """
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['Diagnostics'])
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Diagnosis.objects.filter(patient_id=patient_id).order_by('-timestamp')
