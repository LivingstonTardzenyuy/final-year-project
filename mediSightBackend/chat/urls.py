from django.urls import path
from .views import ConsultationAPI

urlpatterns = [
    path('consult/', ConsultationAPI.as_view(), name='consult'),
]
