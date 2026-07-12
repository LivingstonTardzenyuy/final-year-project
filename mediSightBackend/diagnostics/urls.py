from django.urls import path
from .views import OnlineScanAPI, OfflineSyncAPI, DiagnosticHistoryAPI

urlpatterns = [
    path('scan/', OnlineScanAPI.as_view(), name='scan'),
    path('sync/', OfflineSyncAPI.as_view(), name='sync'),
    path('history/<int:patient_id>/', DiagnosticHistoryAPI.as_view(), name='history'),
]
