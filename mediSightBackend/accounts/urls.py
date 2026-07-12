from django.urls import path
from .views import DoctorRegisterAPI, PatientRegisterAPI, DoctorLoginAPI, PatientLoginAPI, UserAPI, DoctorProfileAPI, PatientProfileAPI, DoctorListAPI

urlpatterns = [
    path('auth/register/doctor/', DoctorRegisterAPI.as_view(), name='register_doctor'),
    path('auth/register/patient/', PatientRegisterAPI.as_view(), name='register_patient'),
    path('auth/login/doctor/', DoctorLoginAPI.as_view(), name='login_doctor'),
    path('auth/login/patient/', PatientLoginAPI.as_view(), name='login_patient'),
    path('auth/user/', UserAPI.as_view(), name='user'),
    path('profile/doctor/', DoctorProfileAPI.as_view(), name='profile_doctor'),
    path('profile/patient/', PatientProfileAPI.as_view(), name='profile_patient'),
    path('doctors/', DoctorListAPI.as_view(), name='list_doctors'),
]
