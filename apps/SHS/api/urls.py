from django.urls import path
from apps.SHS.views import HumedadDeSueloListCreateAPIView, HumedadDeSueloRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', HumedadDeSueloListCreateAPIView.as_view(), name='humedad-suelo-list-create'),
    path('<int:pk>/', HumedadDeSueloRetrieveUpdateDestroyAPIView.as_view(), name='humedad-suelo-detail'),
]