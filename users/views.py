from typing import List

from django.http import JsonResponse
from ninja import Query, Router

from .backend import app
from .models import Person
from .schemas import PageSizeQuerySchema, UserLoginSchema, UserSchema,UserUpdateSchema,ForgotPasswordSchema
from .serializers import TeacherSerializer,StudentSerializer

router = Router()


@router.post("/login", tags=["user login"], summary="user login", auth=None)
def user_login(request, body: UserLoginSchema):
    response, status = app.authenticate_user(body)
    return JsonResponse(response, status=status)


@router.post(
    "/forgot-password",
    tags=["user forgot password"],
    summary="reset user forgotten password",
)
def forgot_password(request,body:ForgotPasswordSchema):
    response,status = app.reset_password(body,request.auth['id'])
    return JsonResponse(response,status=status)


@router.get("/teacher", tags=["teacher"], summary="get list of teachers")
def teacher_list_api_view(request, query_params: PageSizeQuerySchema = Query(...)):
    if request.auth['is_superuser']:
        response, status = app.get(
            request, TeacherSerializer, many=True, is_teacher=True
        )
    elif request.auth['is_teacher']:
        response, status = app.get(
        request, Person, TeacherSerializer, many=False, is_teacher=True, id=request.auth['id']
        )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response,status=status)


@router.post("/teacher", tags=["teacher"], summary="add a teacher")
def teacher_create_api_view(request, body: UserSchema):
    if request.auth['is_superuser']:
        response, status = app.post(body, Person, TeacherSerializer,is_teacher=True)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response,status=status)
    


@router.get(
    "/teacher/{teacher_id}", tags=["teacher"], summary="get a particlar teacher"
)
def teacher_retrive_api_view(request, teacher_id):
    if request.auth['is_superuser']:
        response, status = app.get(
            request, Person, TeacherSerializer, many=False, is_teacher=True, id=teacher_id
        )
    elif request.auth['is_teacher']:
        response, status = app.get(
        request, Person, TeacherSerializer, many=False, is_teacher=True, id=request.auth['id']
        )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.put(
    "/teacher/{teacher_id}",
    tags=["teacher"],
    summary="fully and partial update of a teacher",
)
def teacher_update_api_view(request,teacher_id,body : UserUpdateSchema = None):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response,status = app.put(body,teacher_id)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.delete("/teacher/{teacher_id}", tags=["teacher"], summary="delete a teacher")
def teacher_destroy_api_view(request, teacher_id):
    if any([request.auth['is_superuser']]):
        response, status = app.delete(Person, id=teacher_id)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.get("/student", tags=["student"], summary="get list of students")
def student_list_api_view(request,query_params: PageSizeQuerySchema = Query(...)):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.get(
            request, StudentSerializer, many=True, is_student=True
        )
    elif request.auth['is_student']:
        response, status = app.get(
        request, Person, StudentSerializer, many=False, is_student=True, id=request.auth['id']
    )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.post("/student", tags=["student"], summary="add a student")
def student_create_api_view(request,body:UserSchema):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.post(body, Person, StudentSerializer,is_student=True)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.get(
    "/student/{student_id}", tags=["student"], summary="git a particlar student"
)
def student_retrive_api_view(request,student_id):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.get(
            request, StudentSerializer, many=False, is_student=True, id=student_id
        )
    elif request.auth['is_student']:
        response, status = app.get(
        request, StudentSerializer, many=False, is_student=True, id=request.auth['id']
    )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)

@router.put(
    "/student/{student_id}",
    tags=["student"],
    summary="fully and partial update of a student",
)
def student_update_api_view(request,student_id,body:UserUpdateSchema = None):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response,status = app.put(body,student_id)
    elif request.auth['is_student']:
        response,status = app.put(body,request.auth['id'])
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.delete("/student/{student_id}", tags=["student"], summary="delete a student")
def student_destroy_api_view(request,student_id):
    if any([request.auth['is_superuser']]):
        response, status = app.delete(Person, id=student_id)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)