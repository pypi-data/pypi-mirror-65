"""Declares :class:`JWTService`."""
import datetime
import hashlib
import json

import authlib.jose.errors
import jwt
import jwt.exceptions
from authlib.jose import JsonWebEncryption
from authlib.jose import JWE_ALGORITHMS
from django.conf import settings


class JWTService:
    default_ttl = 0

    @property
    def jwe(self):
        return JsonWebEncryption(algorithms=JWE_ALGORITHMS)

    @property
    def secret(self):
        return hashlib.md5(str.encode(settings.SECRET_KEY)).hexdigest()

    def encrypt(self, payload, sign=True, ttl=None):
        """Sign and encrypt `payload`."""
        protected = {'alg': 'A256GCMKW', 'enc': 'A256GCM'}
        if sign:
            payload = b'1' + self.sign(payload, ttl=ttl)
        else:
            payload = b'0' + str.encode(json.dumps(payload))
        return self.jwe.serialize_compact(protected, payload, self.secret)

    def decrypt(self, cipher):
        """Decrypts the JWE `payload` and verifies the enclosed JWS."""
        try:
            plain = self.jwe.deserialize_compact(cipher, self.secret)
            return plain['payload'][1:], bool(int(plain['payload'][0]))
        except authlib.jose.errors.DecodeError:
            return None, False

    def sign(self, payload, ttl=None):
        """Signs `payload`."""
        if ttl:
            payload['exp'] = datetime.datetime.utcnow()\
                + datetime.timedelta(seconds=ttl)
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode(self, jws, verify=False):
        """Decodes a JSON Web Signature (JWS)."""
        return jwt.decode(jws, self.secret, algorithms=['HS256'])

    def verify(self, jws):
        """Verifies the payload."""
        if jws is None:
            return False
        try:
            self.decode(jws)
            return True
        except jwt.exceptions.PyJWTError:
            return False
