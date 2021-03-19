from ninja.security import APIKeyHeader
from django.conf import settings

class Authorization(APIKeyHeader):
    param_name = settings.JWT_AUTH['JWT_AUTHORIZATION_PREFIX']

    def authenticate(self, request, key):
        if key == "supersecret":
            return key
