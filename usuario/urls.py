from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('dastosUsuario/',include('dastosUsuario.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/',include('allauth.urls')),
    path('registro/', TemplateView.as_view(template_name='loginsocial/log-facebook.html')),
    path('recuperarpass/', include('recuperarpass.urls')),
    path('formcontact/',include('formcontact.urls')),
    path('blog/',include('blog.urls')),
    path('categoriasblog/',include('categoriasblog.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)