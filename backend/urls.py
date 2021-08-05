"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title='APP IDAT',
        default_version= 'v1',
        description = 'Aplicacion para pagina web',
        contact = openapi.Contact(email='A1510732@idat.edu.pe')
    ),
    public=True,
    permission_classes =(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('authentication.urls')),
    path('user_int/',include('info_User.urls')),
    path('cursos/',include('cursos.urls')), 
    path('ecommerce/',include('ecommerce.urls')),
    path('',schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)