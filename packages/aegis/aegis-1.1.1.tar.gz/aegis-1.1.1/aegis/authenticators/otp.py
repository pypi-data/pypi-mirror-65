from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
import hashlib
from aiohttp import web

from ..routes import make_refresh_route
from ..exceptions import InvalidTokenException, TokenExpiredException
from .base import BaseAuthenticator

import pyotp

class OTPAuth(BaseAuthenticator):
    secret: str
    type: str = 'time_based'
    interval = 30
    otp: pyotp.OTP

    async def decode(self, token: str, verify=True) -> dict:
        """Decodes the given token and returns as a dict.
        Raises validation exceptions if verify is set to True."""
        valid = self.otp.verify(token)
        if not valid:
            raise TokenExpiredException()
        return {"otp": token}

    async def get_user(self, credentials) -> dict:
        return credentials

    @abstractmethod
    async def authenticate(self, request: web.Request) -> Dict[str, Any]:
        """Returns JSON serializable user"""

    @classmethod
    def setup(cls, app):
        super().setup(app)
        authenticator: OTP = app["authenticator"]
        otp = pyotp.TOTP(authenticator.secret, authenticator.interval)
        setattr(authenticator, 'otp', otp)
