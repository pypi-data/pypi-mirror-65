import base64
import json

import ioc
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from social_core.exceptions import AuthAlreadyAssociated
from social_core.exceptions import AuthException
from social_core.exceptions import AuthForbidden

import iam.lib.urls
from iam.canon.exc import LoginAborted
from iam.const import MESSAGE_QUERY_PARAM
from iam.domain import FacebookAccountPrincipal
from iam.domain import EmailPrincipal
from iam.domain import GoogleAccountPrincipal
from iam.domain import LinkedInAccountPrincipal
from iam.domain import TwitterAccountPrincipal
from iam.lib.meta import AttributeDispatcher
from iam.ext.django.models import Realm
from iam.ext.django.models import Subject
from iam.ext.django.models import SubjectRegistration


def on_redirected(request, backend, *args, **kwargs):
    """Invoked directly when the SSO redirects back to our application."""
    response = None
    state = json.loads(bytes.decode(
        base64.urlsafe_b64decode(request.GET['state'])))
    if not state.get('payload'):
        request.realm = settings.IAM_REALM
    else:
        jwt = ioc.require('JWTService')
        payload, signed = jwt.decrypt(state['payload'])
        if not signed\
        or not payload\
        or (payload and signed and not jwt.verify(payload)):
            # This in all cases indicates tampering.
            payload = {'rlm': 'jail', 'reason': 'tamper'}
        else:
            payload = jwt.decode(payload)

        if payload.get('rlm') == 'jail':
            return HttpResponseRedirect(iam.lib.urls.reverse('login'))

        assert 'rlm' in payload
        request.realm = payload['rlm']

    realm = Realm.objects.get(name=request.realm)

    # Check if the realm allows login using this SSO.
    if not realm.allowsso(backend.name):
        messages.error(request, _("This provider is temporarily disabled."))
        return HttpResponseRedirect(iam.lib.urls.reverse('login'))


def on_authenticated(request, strategy, details, backend, *args, **kwargs):
    """Invoked when a user authenticates through the SSO provider."""
    resolver = IdentityProviderSubjectResolver()
    subject = None
    kwargs['request'] = request
    kwargs['realm'] = request.realm
    kwargs['site'] = request.site
    kwargs['host'] = request.host
    if request.user.is_authenticated:
        subject = request.user
    try:
        with transaction.atomic():
            uid, subject, new, social = resolver.resolve(
                backend, details, subject, *args, **kwargs)
    except LoginAborted as e:
        messages.error(request, e.reason)
        return HttpResponseRedirect(e.redirect_to)

    return {
        'social': social,
        'uid': uid,
        'user': subject,
        'is_new': new,
        'new_association': social is None
    }


class IdentityProviderSubjectResolver:

    @AttributeDispatcher.dispatch('name')
    def resolve(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    @resolve.register('facebook')
    def resolve(self, backend, details, subject, response, is_new,
        *args, **kwargs):
        """Resolve a :term:`Subject` using a Google OAuth2 response.

        Args:
            backend (:class:`~social_core.backends.twitter.TwitterOAuth`): the
                :mod:`social_core` backend used to authenticate the subject.
            details (:obj:`dict`): a dictionary containing user details that
                were discovered by previous steps in the
                :term:`Authentication Pipeline`. In the default implementation,
                this is an empty dictionary.
            response (:obj:`dict`): the response that was received from Google.
            pipeline_index (:obj:`int`): indicates the position in the
                :term:`Authentication Pipeline` where this function was invoked.
                In the default implementation, `pipeline_index` is always ``0``.
            is_new (:obj:`bool`): indicates if the authenticated :term:`Subject`
                is a new user.
            **kwargs: keyword arguments not worthy of documentation.

        Returns:
            :obj:`tuple`
        """
        kwargs['platform'] = 'facebook'
        return self.process_response(FacebookAccountPrincipal.fromoauth2, backend,
            details, subject, response, is_new, *args, **kwargs)

    @resolve.register('google-oauth2')
    def resolve(self, backend, details, subject, response, is_new,
        *args, **kwargs):
        """Resolve a :term:`Subject` using a Google OAuth2 response.

        Args:
            backend (:class:`~social_core.backends.google.GoogleOAuth2`): the
                :mod:`social_core` backend used to authenticate the subject.
            details (:obj:`dict`): a dictionary containing user details that
                were discovered by previous steps in the
                :term:`Authentication Pipeline`. In the default implementation,
                this is an empty dictionary.
            response (:obj:`dict`): the response that was received from Google.
            pipeline_index (:obj:`int`): indicates the position in the
                :term:`Authentication Pipeline` where this function was invoked.
                In the default implementation, `pipeline_index` is always ``0``.
            is_new (:obj:`bool`): indicates if the authenticated :term:`Subject`
                is a new user.
            **kwargs: keyword arguments not worthy of documentation.

        Returns:
            :obj:`tuple`
        """
        if bool(response.get('email_verified')):
            kwargs['email'] = EmailPrincipal(response['email'])
        if response.get('hd'):
            kwargs['domain'] = response['hd']
        kwargs['first_name'] = response.get('given_name')
        kwargs['last_name'] = response.get('family_name')
        kwargs['platform'] = 'google'
        return self.process_response(GoogleAccountPrincipal.fromoauth2, backend,
            details, subject, response, is_new, *args, **kwargs)

    @resolve.register('linkedin-oauth2')
    def resolve(self, backend, details, subject, response, is_new,
        *args, **kwargs):
        """Resolve a :term:`Subject` using a LinkedIn OAuth2 response.

        Args:
            backend (:class:`~social_core.backends.twitter.TwitterOAuth`): the
                :mod:`social_core` backend used to authenticate the subject.
            details (:obj:`dict`): a dictionary containing user details that
                were discovered by previous steps in the
                :term:`Authentication Pipeline`. In the default implementation,
                this is an empty dictionary.
            response (:obj:`dict`): the response that was received from Google.
            pipeline_index (:obj:`int`): indicates the position in the
                :term:`Authentication Pipeline` where this function was invoked.
                In the default implementation, `pipeline_index` is always ``0``.
            is_new (:obj:`bool`): indicates if the authenticated :term:`Subject`
                is a new user.
            **kwargs: keyword arguments not worthy of documentation.

        Returns:
            :obj:`tuple`
        """
        kwargs['platform'] = 'linkedin'
        return self.process_response(LinkedInAccountPrincipal.fromoauth2, backend,
            details, subject, response, is_new, *args, **kwargs)

    @resolve.register('twitter')
    def resolve(self, backend, details, subject, response, is_new,
        *args, **kwargs):
        """Resolve a :term:`Subject` using a Google OAuth2 response.

        Args:
            backend (:class:`~social_core.backends.twitter.TwitterOAuth`): the
                :mod:`social_core` backend used to authenticate the subject.
            details (:obj:`dict`): a dictionary containing user details that
                were discovered by previous steps in the
                :term:`Authentication Pipeline`. In the default implementation,
                this is an empty dictionary.
            response (:obj:`dict`): the response that was received from Google.
            pipeline_index (:obj:`int`): indicates the position in the
                :term:`Authentication Pipeline` where this function was invoked.
                In the default implementation, `pipeline_index` is always ``0``.
            is_new (:obj:`bool`): indicates if the authenticated :term:`Subject`
                is a new user.
            **kwargs: keyword arguments not worthy of documentation.

        Returns:
            :obj:`tuple`
        """
        kwargs['platform'] = 'twitter'
        return self.process_response(TwitterAccountPrincipal.fromoauth2, backend,
            details, subject, response, is_new, *args, **kwargs)

    def process_response(self, principal_factory, backend, details, subject, response, is_new, *args, **kwargs):
        """Resolve a :term:`Subject` using an OAuth2 response.

        Args:
            backend (:class:`~social_core.backends.oauth.OAuthAuth`): the
                :mod:`social_core` backend used to authenticate the subject.
            details (:obj:`dict`): a dictionary containing user details that
                were discovered by previous steps in the
                :term:`Authentication Pipeline`. In the default implementation,
                this is an empty dictionary.
            response (:obj:`dict`): the response that was received from from
                the :term:`Identity Provider`.
            pipeline_index (:obj:`int`): indicates the position in the
                :term:`Authentication Pipeline` where this function was invoked.
                In the default implementation, `pipeline_index` is always ``0``.
            is_new (:obj:`bool`): indicates if the authenticated :term:`Subject`
                is a new user.
            **kwargs: keyword arguments not worthy of documentation.

        Returns:
            :obj:`tuple`
        """
        domain = kwargs.pop('domain', None)
        site = kwargs.pop('site')
        srcaddr = kwargs.pop('host')
        platform = kwargs.pop('platform')
        is_new = bool(kwargs.get('is_new'))
        realm = kwargs.pop('realm') or settings.IAM_REALM
        request = kwargs.pop('request')
        principal = principal_factory(response)
        social = backend.strategy.storage.user.get_social_auth(
            backend.name, principal.inrealm(realm))

        # TODO: All of this logic needs to be hidden behind service classes.
        config = settings.IAM_REALM_SETTINGS.get(realm)
        if not config.get('public'):
            # The realm is not public, check if the domain is whitelisted.
            if domain not in config.get('domains'):
                raise LoginAborted(
                    redirect_to=iam.lib.urls.reverse('login'),
                    reason=_("You are trying to access a protected area for "
                             "which you do not have access permissions."))

        # Check if a social account is associated to a user. If the user was
        # logged in and the social account is not yet associated, then
        # associate it with the user account.
        if social:
            if subject and social.user != subject:
                # Authenticated user that tries to associate a social account
                # that is already associated.
                raise AuthAlreadyAssociated("This account is already in use.")
            elif not subject:
                # Unauthenticated user that came in with a social account
                # that was previously associated.
                subject = social.user

        # Allow the lookup of subjects by some common principals. We have
        # validated and trust these principals.
        principals = [
            kwargs.pop('email', None)
        ]
        for p in principals:
            if p is None:
                continue
            try:
                subject = Subject.objects.get_by_principal(realm, p)
            except Subject.DoesNotExist:
                continue
            else:
                # Should not happen, but indicates that an other user has
                # claimed this principal.
                if social and (subject != social.user):
                    raise LoginAborted(
                        redirect_to=iam.lib.urls.reverse('login'),
                        reason=_("Unable to authenticate with the given credentials."))
                break

        # If subject is still None, create one.
        if subject is None:
            try:
                subject = principal.resolve(realm, Subject.objects)
            except Subject.DoesNotExist:
                is_new = True
                subject = Subject.objects.create(realm_id=realm)

                # TODO: Implement RegistrationService
                SubjectRegistration.objects.create(
                    using_id=subject.addprincipal(principal),
                    host=srcaddr,
                    platform=site.domain
                )

            assert subject.realm_id == realm

            # See if we can set up the account.
            if kwargs.get('first_name'):
                subject.first_name = kwargs.get('first_name')
            if kwargs.get('last_name'):
                subject.last_name = kwargs.get('last_name')

        elif subject and not social:
            subject.addprincipal(principal)

        if subject and subject.realm_id != realm:
            # Something went horribly wrong.
            raise NotImplementedError

        return principal.inrealm(realm), subject, is_new, social
