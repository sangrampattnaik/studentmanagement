import jwt
from django.conf import settings
from ninja.security import APIKeyHeader


class Authorization(APIKeyHeader):
    '''
    Authorization by using JWT token
    '''
    param_name = settings.JWT_AUTH['JWT_AUTHORIZATION_HEADER_KEY']

    def authenticate(self, request, key):
        try:
            header,token = key.split(" ")
            if header == settings.JWT_AUTH['JWT_AUTHORIZATION_HEADER_PREFIX']:
                payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
                return payload
        except (jwt.exceptions.DecodeError,ValueError,jwt.exceptions.InvalidSignatureError,jwt.exceptions.ExpiredSignatureError,jwt.exceptions.InvalidTokenError,AttributeError):
            pass

