from django.urls import path
from apps.ST.views import TemperaturaListCreateAPIView, TemperaturaRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('',TemperaturaListCreateAPIView.as_view(),name='temperatura-list-create'),
    path('<int:pk>/',TemperaturaRetrieveUpdateDestroyAPIView.as_view(),name='temperatura-detail'),
]