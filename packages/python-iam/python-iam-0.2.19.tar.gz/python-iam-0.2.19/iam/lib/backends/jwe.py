"""Declares :class:`JWEStateMixin`."""
import base64
import datetime
import json

import ioc
from django.conf import settings
from django.utils.crypto import constant_time_compare
from unimatrix.lib import timezone

from iam.const import MESSAGE_TOKEN_SESSION_KEY


class JWEStateMixin:
    STATE_PARAMETER = True
    jwt = ioc.class_property('JWTService')

    def start(self, *args, **kwargs):
        """Starts OAuth2 process."""
        # Pop the session state token so we are sure that a new value is generated
        # on every login.
        self.strategy.session_pop(self.name + '_state')
        return super().start(*args, **kwargs)

    def state_token(self):
        """Generate csrf token to include as state parameter."""
        state = {
            'token': super().state_token()
        }

        # Instead of simply using a token, we send base64 URL-encoded string
        # containing the content of the `payload` query parameter, and the
        # token. The `payload` parameter, if provided, is a JWS containing a
        # payload, signed with settings.SECRET_KEY
        params = self.strategy.request_data()
        token = self.strategy.session_pop(MESSAGE_TOKEN_SESSION_KEY) or ''
        if params.get('payload'):
            # Verify the payload and validate the signature.
            payload, signed = self.jwt.decrypt(str.encode(params['payload']))
            if payload is None or not self.jwt.verify(payload):
                # The payload has been tampered with. Replace it with our own
                # payload and allow the process to continue. When the user
                # redirects from the SSO, we will have its login credentials
                # and can take further action.
                payload = {'rlm': 'jail', 'why': 'tamper'}
            elif signed and payload:
                payload = self.jwt.decode(payload)

                # Check if the token matches the one set in the session.
                if not constant_time_compare(token, payload.get('token') or ''):
                    payload = {'rlm': 'jail', 'why': 'tamper'}

            # Resign and encrypt the payload with an expiry.
            payload = self.jwt.encrypt(payload, sign=True, ttl=60)
            state['payload'] = bytes.decode(payload)
        return base64.urlsafe_b64encode(str.encode(json.dumps(state)))
