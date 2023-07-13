from django.urls import path
from apps.plants.views import PlantaList, PlantaCreate,PlantaRetrieveUpdateDestroy

urlpatterns = [
    path('', PlantaList.as_view(), name='plant-list'),
    path('create/', PlantaCreate.as_view(), name='plant-create'),
    path('<int:pk>/', PlantaRetrieveUpdateDestroy.as_view(), name='plant-retrieve-update-destroy'),
]
