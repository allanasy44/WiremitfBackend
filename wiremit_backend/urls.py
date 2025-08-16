from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
def health(_): return JsonResponse({'status':'ok'})
schema_view = get_schema_view(openapi.Info(title="Wiremit API", default_version="v1"), public=True, permission_classes=(permissions.AllowAny,))
urlpatterns=[path('admin/',admin.site.urls), path('health/',health), path('api/', include('users.urls')), path('api/', include('rates.urls')), re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),]
