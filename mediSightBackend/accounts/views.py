from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, DoctorRegisterSerializer, PatientRegisterSerializer, DoctorLoginSerializer, PatientLoginSerializer, DoctorProfileSerializer, PatientProfileSerializer
from .models import DoctorProfile, PatientProfile

class DoctorRegisterAPI(generics.GenericAPIView):
    """
    Register a new Doctor account. 
    The provided email will be used as the username.
    """
    serializer_class = DoctorRegisterSerializer

    @extend_schema(tags=['Authentication'], responses={201: UserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class PatientRegisterAPI(generics.GenericAPIView):
    """
    Register a new Patient account.
    """
    serializer_class = PatientRegisterSerializer

    @extend_schema(tags=['Authentication'], responses={201: UserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class DoctorLoginAPI(generics.GenericAPIView):
    """
    Log in with Doctor credentials (email & password).
    """
    serializer_class = DoctorLoginSerializer

    @extend_schema(tags=['Authentication'], responses={200: UserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_200_OK)

class PatientLoginAPI(generics.GenericAPIView):
    """
    Log in with Patient credentials (username & password).
    """
    serializer_class = PatientLoginSerializer

    @extend_schema(tags=['Authentication'], responses={200: UserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_200_OK)

class UserAPI(generics.RetrieveAPIView):
    """
    Get the details of the currently authenticated user.
    Requires a valid Token in the Authorization header.
    """
    @extend_schema(tags=['Authentication'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class DoctorProfileAPI(generics.RetrieveUpdateAPIView):
    """
    Get or update the profile of the currently authenticated doctor.
    """
    @extend_schema(tags=['Profiles'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=['Profiles'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=['Profiles'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorProfileSerializer

    def get_object(self):
        profile, created = DoctorProfile.objects.get_or_create(user=self.request.user)
        return profile

class PatientProfileAPI(generics.RetrieveUpdateAPIView):
    """
    Get or update the profile of the currently authenticated patient.
    """
    @extend_schema(tags=['Profiles'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=['Profiles'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=['Profiles'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientProfileSerializer

    def get_object(self):
        profile, created = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

class DoctorListAPI(generics.ListAPIView):
    """
    Get a list of all registered doctors.
    """
    @extend_schema(tags=['Profiles'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        from .models import User
        return User.objects.filter(role=User.Role.DOCTOR, is_active=True)

