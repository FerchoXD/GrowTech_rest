from django.urls import path
from apps.SIL.views import IntensidadDeLuzListCreateAPIView, IntensidadDeLuzRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', IntensidadDeLuzListCreateAPIView.as_view(), name='intensidad-list-create'),
    path('<int:pk>/', IntensidadDeLuzRetrieveUpdateDestroyAPIView.as_view(), name='intensidad-detail'),
]