from django.contrib.auth import authenticate
import datetime
import jwt
from django.conf import settings

def get_token(user):
    td = timedelta(
        days=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_DAYS"],
        hours=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_HOURS"],
        minutes=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES"],
        seconds=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS"],
    )
    payload = {
        "id": person.id,
        "exp": datetime.utcnow() + td,
        "role_id": person.role_id.role_id,
        "school_code": person.school_code,
    }
    self.token = jwt.encode(payload, settings.SECRET_KEY, "HS256")
    self.person_serialized_data = serializer(person).data
    return self.token, self.person_serialized_data


def authenticate_user(body):
    body = body.dict()
    user = authenticate(username=body['username'],password=body['password'])
    if user:
        return {"status":"success"}
    return {"status":"failed","msg":"authentication failed","error":"username or password incorrect"}