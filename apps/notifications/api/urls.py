from django.urls import path
from apps.notifications.views import NotificacionListCreateAPIView, NotificacionRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', NotificacionListCreateAPIView.as_view(), name='notificacion-list-create'),
    path('<int:pk>/', NotificacionRetrieveUpdateDestroyAPIView.as_view(), name='notificacion-detail'),
]