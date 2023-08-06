"""Specifies the URLs exposed by the :mod:`iam.ext.django` application."""
from django.urls import include
from django.urls import path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from . import views


app_name = 'iam'

urlpatterns = []
if settings.DEBUG or settings.IAM_ENABLE_DEBUG_PAGE:
    handler = views.DebugView.as_view()
    urlpatterns += [
        path(str.lstrip(settings.IAM_DEBUG_PATH, '/'),
            login_required(handler), name='debug')
    ]


urlpatterns.extend([
    path('forms/',
        include(([
            path('names', views.ChooseNamesFormView.as_view(), name='names'),
            path('accept/terms', views.AcceptAgreementFormView.as_view(),
                name='terms'),
        ], 'iam'), namespace='forms'),
    ),
    path(_('login/'), views.LoginView.as_view(allow_public=True), name='login'),
    path(_('login/magic'), views.MagicLinkView.as_view(), name='login.magic'),
    path(_('login/token'), views.LoginTokenView.as_view(), name='login.token'),
    path(_('logout'), views.LogoutView.as_view(), name='logout'),
    path(_('register'), views.RegisterView.as_view(), name='register'),
])

if settings.IAM_ENABLE_PASSWORD_RESET:
    urlpatterns.append(
        path(_('login/reset'), views.ResetCredentialsView.as_view(),
            name='resetcredentials'))
