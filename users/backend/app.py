import datetime
import re

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404

from users.models import Person


def password_validation(password):
    '''
    password validation like minimum 8 to 20 chars including digit, special char, upper case and lower case

    params:
        password : str
    
    return 
        bool : True / False
        error message : str
    '''
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    mat = re.fullmatch(reg, password)
    if mat:
        return True, password
    return (
        False,
        "Password should have atleast 8 characters, one upper case, one lower case, one digit and one special character",
    )

def reset_password(body,id):
    '''
    user can reset password 

    params:
        body : dict (old_password , new_password and confirm_password) 
        id: int
    
    return 
        response : user response
        status_code : int
    '''
    body = body.dict()
    user = get_object_or_404(User,id=id)
    if body['new_password'] != body['confirm_password']:
        return {"status":"failed",'msg':"new password and confirm password should be matched"},400
    error,msg = password_validation(body['new_password'])
    if not error:
        return {"status":"failed",'msg':error},400
    auth_user = authenticate(username=user.username,password=body['old_password'])
    print(auth_user)
    if auth_user:
        user.set_password(body['new_password'])
        user.save()
        return {"status":"success",'msg':"new password updated"},200
    else:
        return {"status":"failed",'msg':"incorrect old password"},400


def email_validation(email):
    '''
    email validation like @ and domain

    params:
        email : str
    
    return 
        bool : True / False
        error message : str
    '''
    regex = "[a-zA-Z]+.*@.+[.].+$"
    match = re.fullmatch(regex, email)
    if User.objects.filter(email=email).exists():
        return False, "email already registerd"
    if not match:
        return False, "Invalid Email"
    return True, None

def paginate(request, queryset, Serializer):
    '''
    pagination of data according to page and size

    params:
        request : end user request
        queryset : models queryset
        serializer : serilization class
    
    return 
        count : int
        next_page : url
        previous_page : url,
        data : serialized response data
    '''

    try:
        if (count := len(queryset)) == 0:
            return [], 0, "", ""
        page_and_size = ["page", "size"]
        query_params = request.GET.dict().copy()
        for page_name in page_and_size:
            if page_name in query_params:
                query_params.pop(page_name)
        other_query_params = ""
        for key, value in query_params.items():
            other_query_params += f"&{key}={value}"
        path = request.path
        host = request.get_host()
        http = "https://" if request.is_secure() else "http://"
        page = int(request.GET.get("page"))
        size = int(request.GET.get("size"))
        site = f"{http}{host}{path}"
        next_page = ""
        previous_page = ""
        if page == 1:
            if count > page * size:
                next_page = site + f"?page={page + 1}&size={size}" + other_query_params
            else:
                next_page = ""
        elif page * size > count:
            previous_page = ""
        elif page * size >= count:
            previous_page = site + f"?page={page - 1}&size={size}" + other_query_params
        else:
            previous_page = site + f"?page={page - 1}&size={size}" + other_query_params
            next_page = site + f"?page={page + 1}&size={size}" + other_query_params
        serialized_data = Serializer(
            queryset[page * size - size : page * size], many=True
        ).data
        return serialized_data, count, next_page, previous_page
    except ValueError:
        return None, None, "invalid page or size", "invalid page or size"


def get_token(user):
    '''
    generate a JWT token

    params:
        user : db user object
    
    return 
        token : str (JWT token)
    '''
    td = datetime.timedelta(
        days=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_DAYS"],
        hours=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_HOURS"],
        minutes=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES"],
        seconds=settings.JWT_AUTH["JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS"],
    )
    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + td,
        "is_superuser": user.is_superuser,
        "is_student": user.person_user.is_student,
        "is_teacher": user.person_user.is_teacher,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, "HS256")
    return token


def authenticate_user(body):
    '''
    authenticate user by username and password

    params:
        body : dict (username and password)
    
    return 
        token : str (JWT token)
        status_code : int
    '''
    body = body.dict()
    user = authenticate(username=body["username"], password=body["password"])
    if user:
        token = get_token(user)
        return {"token": token, "status": "success"}, 200
    return {
        "status": "failed",
        "msg": "authentication failed",
        "err": "incorrect username or password",
    }, 401


def get(request, Serializer, many=False, **kwargs):
    '''
    get data from database and send serialized response

    params:
        request : end user request
        Serializer : data serialization
        many : bool (True / False) = True to serilaize list of records and False to serialize a single record
        kwargs : dict (model fields)
    
    return 
        response : dict
        status_code : int
        
    '''
    if many:
        queryset = Person.objects.filter(**kwargs)
        serialized_data, count, next_page, previous_page = paginate(
            request, queryset, Serializer
        )
        return {
            "count": count,
            "next_page": next_page,
            "previous_page": previous_page,
            "data": serialized_data,
        }, 200
    else:
        teacher = get_object_or_404(Model, **kwargs)
        serialized_data = Serializer(teacher).data
        return {"status": "success", "data": serialized_data}, 200


def post(body, Person, Serializer, is_teacher=False, is_student=False):
    '''
    get data from database and send serialized response

    params:
        request : end user request
        Serializer : data serialization
        many : bool (True / False) = True to serilaize list of records and False to serialize a single record
        kwargs : dict (model fields)
    
    return 
        response : dict
        status_code : int
        
    '''
    body = body.dict()
    if User.objects.filter(username=body["username"]).exists():
        return {"status": "failed", "msg": "username already taken"}, 400
    error,msg = email_validation(body['email'])
    if not error:
        return {"status": "failed", "msg": msg}, 400
    error_in_pwd,msg = password_validation(body['password'])
    if not error_in_pwd:
        return {"status": "failed", "msg": msg}, 400
    if is_teacher:
        person = Person.create_teacher(
            username=body["username"],
            password=body["password"],
            email=body["email"],
            first_name=body["first_name"],
            last_name=body["last_name"],
        )
    elif is_student:
        person = Person.create_student(
            username=body["username"],
            password=body["password"],
            email=body["email"],
            first_name=body["first_name"],
            last_name=body["last_name"],
        )
    else:
        return {"status": "failed"}, 400
    serialized_data = Serializer(person).data
    return {"status": "success", "msg": "teacher created", "data": serialized_data}, 201


def delete(**kwargs):
    '''
    delete user data from database

    params:
        kwargs : dict (model fields like id)
    return 
        response : dict
        status_code : int
        
    '''
    person = get_object_or_404(Person, **kwargs)
    User.objects.filter(id=person.user.id).delete()
    person.delete()
    return {"status": "success", "msg": "user deleted"}, 200



def put(body,id):
    '''
    update user data

    params:
        body : dict (user model fields)
        id : int 
    return 
        response : dict
        status_code : int
        
    '''
    person = get_object_or_404(Person, id=id)
    user = User.objects.get(username=person.user.username)
    body = body.dict()
    username = body.get('username')
    email = body.get('email')
    last_name = body.get('last_name')
    first_name = body.get('first_name')

    if username:
        if username != person.user.username:
            if not User.objects.filter(username=username).exists():
                user.username = username
    if email:
        if email != person.user.email:
            error,msg = email_validation(body['email'])
            if not error:
                return {"status": "failed", "msg": msg}, 400
            else:
                user.email = body['email']
    if last_name:
        user.last_name = last_name
    if first_name:
        user.first_name = first_name
    user.save()
    person.save()
    return {"status":"success",'msg':"user updated"},200
