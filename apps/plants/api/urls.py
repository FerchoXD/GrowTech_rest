from django.urls import path
from apps.plants.views import PlantaList, PlantaCreate,PlantaRetrieveUpdateDestroy,ValidacionPlants,PlantaListByUser,DatosPromedios,PlantaConsultaView,PlantaView

urlpatterns = [
    path('', PlantaList.as_view(), name='plant-list'),
    path('create/', PlantaCreate.as_view(), name='plant-create'),
    path('<int:pk>/', PlantaRetrieveUpdateDestroy.as_view(), name='plant-retrieve-update-destroy'),
    path('validar/planta/',ValidacionPlants.as_view(),name= 'planta-validacion'),
    path('listar/plantas/<int:id>/', PlantaListByUser.as_view(), name='planta-listar-por-usuario'),
    path('obtener-datos-promedio/', DatosPromedios.as_view(), name='datos-promedio'),
    path('consulta/<int:id>/', PlantaConsultaView.as_view(), name='consulta_plantas'),
    path('status-estadistico/', PlantaView.as_view(), name='status-estadistico'),
]
