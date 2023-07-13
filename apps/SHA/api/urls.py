from django.urls import path
from apps.SHA.views import HumedadDeAmbienteListCreateAPIView, HumedadDeAmbienteRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', HumedadDeAmbienteListCreateAPIView.as_view(), name='humedad-ambiente-list-create'),
    path('<int:pk>/', HumedadDeAmbienteRetrieveUpdateDestroyAPIView.as_view(), name='humedad-ambiente-detail'),
]