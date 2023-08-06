"""Specifies the URLs for the :mod:`iam` demo project."""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

from ..django import views


urlpatterns = [
    path('auth/', include('social_django.urls',
        namespace=settings.SOCIAL_AUTH_URL_NAMESPACE)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('admin/login/', views.LoginView.as_view(
        allow_signup=False,
        allow_local=False,
        realm=settings.IAM_STAFF_REALM,
        allow_public=False
    )),
    path('admin/', admin.site.urls),
    path('', include('iam.ext.django.urls',
        namespace=settings.IAM_URL_NAMESPACE))
)

admin.autodiscover()
