from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.views import Login,Logout,Register,EmailSenderView
from apps.plants.api.urls import urlpatterns 
from apps.SIL.api.urls import urlpatterns
from apps.GenerarReporte.api.urls import urlpatterns
schema_view = get_schema_view(
   openapi.Info(
      title="Documentación de API",
      default_version='v0.1',
      description="Documentación pública de API de GrowTech",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="213524@ids.upchiapas.edu.mx"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('logout/', Logout.as_view(), name = 'logout'),
   path('login/',Login.as_view(), name = 'login'),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('users/',include('apps.users.api.routers')),
   path('register/', Register.as_view(), name='register'),
   path('plants/', include('apps.plants.api.urls')),
   path('intensidad/', include('apps.SIL.api.urls')),
   path('temperatura/', include('apps.ST.api.urls')),
   path('humedad/suelo/', include('apps.SHS.api.urls')),
   path('humedad/ambiente/', include('apps.SHA.api.urls')),
   path('notificacion/', include('apps.notifications.api.urls')),
   path('generar/',include('apps.GenerarReporte.api.urls')),
   path('email-sender/', EmailSenderView.as_view(), name='email-sender'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
