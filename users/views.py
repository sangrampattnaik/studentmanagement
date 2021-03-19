from typing import List

from django.http import JsonResponse
from ninja import Query, Router

from .backend import app
from .models import Person
from .schemas import (ForgotPasswordSchema, PageSizeQuerySchema,
                      UserLoginSchema, UserSchema, UserUpdateSchema)
from .serializers import StudentSerializer, TeacherSerializer

router = Router()


@router.post("/login", tags=["user login"], summary="user login",
    description = "super admin , teacher and student can get login token by providing correct username and password"
, auth=None)
def user_login(request, body: UserLoginSchema):
    response, status = app.authenticate_user(body)
    return JsonResponse(response, status=status)


@router.post(
    "/forgot-password",
    tags=["user forgot password"],
    summary="reset user forgotten password",
    description = "super admin , teacher and student can reset password"
)
def forgot_password(request,body:ForgotPasswordSchema):
    response,status = app.reset_password(body,request.auth['id'])
    return JsonResponse(response,status=status)


@router.get("/teacher", tags=["teacher"], summary="get list of teachers",
    description = "super admin ,get list of teacher and  teacher can get only his information"
)
def teacher_list(request, query_params: PageSizeQuerySchema = Query(...)):
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


@router.post("/teacher", tags=["teacher"], summary="add a teacher",
    description = "only super admin can add a teacher"
)
def teacher_create(request, body: UserSchema):
    if request.auth['is_superuser']:
        response, status = app.post(body, Person, TeacherSerializer,is_teacher=True)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response,status=status)
    


@router.get(
    "/teacher/{teacher_id}", tags=["teacher"], summary="get a particlar teacher",
    description = "only super admin can retrive prticular a teacher."
)
def teacher_get(request, teacher_id):
    if request.auth['is_superuser']:
        response, status = app.get(
            request, Person, TeacherSerializer, many=False, is_teacher=True, id=teacher_id
        )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.put(
    "/teacher/{teacher_id}",
    tags=["teacher"],
    summary="fully and partial update of a teacher",
    description = "only super admin can update prticular teacher if teacher, he can only update his info"

)
def teacher_update(request,teacher_id,body : UserUpdateSchema = None):
    if any([request.auth['is_superuser']]):
        response,status = app.put(body,teacher_id)
    elif request.auth['is_teacher']:
        response,status = app.put(body,request.auth['id'])
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.delete("/teacher/{teacher_id}", tags=["teacher"], summary="delete a teacher",
    description = "only super admin can delete a teacher"
)
def teacher_delete(request, teacher_id):
    if any([request.auth['is_superuser']]):
        response, status = app.delete(id=teacher_id)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.get("/student", tags=["student"], summary="get list of students",
    description = "only super admin can and teacher can view list of students"
)
def student_list(request,query_params: PageSizeQuerySchema = Query(...)):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.get(
            request, StudentSerializer, many=True, is_student=True
        )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.post("/student", tags=["student"], summary="add a student",
    description = "only super admin and teacher can add a student"
)
def student_create(request,body:UserSchema):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.post(body, Person, StudentSerializer,is_student=True)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.get(
    "/student/{student_id}", tags=["student"], summary="git a particlar student",
    description = "only super admin and teacher can view a particular student"
)
def student_get(request,student_id):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response, status = app.get(
            request, StudentSerializer, many=False, is_student=True, id=student_id
        )
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)

@router.put(
    "/student/{student_id}",
    tags=["student"],
    summary="fully and partial update of a student",
    description = "only super admin ,teacher can view a particular student"
)
def student_update(request,student_id,body:UserUpdateSchema = None):
    if any([request.auth['is_superuser'],request.auth['is_teacher']]):
        response,status = app.put(body,student_id)
    elif request.auth['is_student']:
        response,status = app.put(body,request.auth['id'])
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)


@router.delete("/student/{student_id}", tags=["student"], summary="delete a student",
    description = "only super admin can delete a particular student"
)
def student_delete(request,student_id):
    if any([request.auth['is_superuser']]):
        response, status = app.delete(id=student_id)
    else:
        response = {"status":"failed","msg":"permission denied"}
        status = 403
    return JsonResponse(response, status=status)