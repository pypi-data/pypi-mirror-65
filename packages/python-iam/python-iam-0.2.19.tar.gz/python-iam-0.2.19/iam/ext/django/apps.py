"""Bootstraps the :mod:`iam.ext.django` Django application."""
import ioc
from django.apps import AppConfig

from . import infra
from . import services


class IAMConfig(AppConfig):
    name = 'iam.ext.django'
    label= 'iam'

    def ready(self):
        ioc.provide('AgreementAcceptanceService',
            services.AgreementAcceptanceService())
        ioc.provide('CredentialService', services.CredentialService())
        ioc.provide('HashedPasswordRepository',
            infra.HashedPasswordRepository())
        ioc.provide('JWTService', services.JWTService())
        ioc.provide('OneTimePasswordService',
            services.OneTimePasswordService())
        ioc.provide('PasswordService',
            services.PasswordService())
        ioc.provide('PasswordResetService',
            services.PasswordResetService())
        ioc.provide('PrincipalAvailabilityService',
            services.PrincipalAvailabilityService())
        ioc.provide('RegistrationService', services.RegistrationService())
        ioc.provide('SubjectRepository', infra.SubjectRepository())
        ioc.provide('iam.TemplateService', services.TemplateService())
