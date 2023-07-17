from django.urls import path
from apps.ST.views import TemperaturaListCreateAPIView, TemperaturaRetrieveUpdateDestroyAPIView,UltimoDatoTemperaturaAPIView

urlpatterns = [
    path('',TemperaturaListCreateAPIView.as_view(),name='temperatura-list-create'),
    path('<int:pk>/',TemperaturaRetrieveUpdateDestroyAPIView.as_view(),name='temperatura-detail'),
    path('temperaturas/ultimo-dato/', UltimoDatoTemperaturaAPIView.as_view(), name='ultimo-dato-temperatura'),
]