from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.rooms.urls')),
    path('api/', include('apps.reservations.urls')),
    path('api/', include('apps.payments.urls')),
    path('api/', include('apps.accounts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api-docs'),    
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="api_schema"), name="redoc"),
    

]
