from typing import List

from django.http import JsonResponse
from ninja import Query, Router

from .backend import app
from .models import Person
from .schemas import PageSizeQuerySchema, UserLoginSchema, UserSchema
from .serializers import TeacherSerializer

router = Router()


@router.post("/login", tags=["user login"], summary="user login", auth=None)
def user_login(request, body: UserLoginSchema):
    response, status = app.authenticate_user(body)
    return JsonResponse(response, status=status)


@router.post(
    "/forgot-password",
    tags=["user forgot password"],
    summary="reset user forgotten password",
    auth=None,
)
def forgot_password(request):
    print(request.auth)


@router.get("/teacher", tags=["teacher"], summary="get list of teachers")
def teacher_list_api_view(request, query_params: PageSizeQuerySchema = Query(...)):
    response, status = app.get(
        request, Person, TeacherSerializer, many=True, is_teacher=True
    )
    return JsonResponse(response, status=status)


@router.post("/teacher", tags=["teacher"], summary="create a teacher")
def teacher_create_api_view(request, body: UserSchema):
    response, status = app.post(body, Person, TeacherSerializer)
    return JsonResponse(response, status=status)


@router.get(
    "/teacher/{teacher_id}", tags=["teacher"], summary="get a particlar teacher"
)
def teacher_retrive_api_view(request, teacher_id):
    response, status = app.get(
        request, Person, TeacherSerializer, many=False, is_teacher=True, id=teacher_id
    )
    return JsonResponse(response, status=status)


@router.put(
    "/teacher/{teacher_id}",
    tags=["teacher"],
    summary="fully and partial update of a teacher",
)
def teacher_update_router_view(request):
    pass


@router.delete("/teacher/{teacher_id}", tags=["teacher"], summary="delete a teacher")
def teacher_destroy_api_view(request, teacher_id):
    response, status = app.delete(Person, id=teacher_id)
    return JsonResponse(response, status=status)


@router.get("/student", tags=["student"], summary="get list of students")
def student_list_api_view(request):
    pass


@router.post("/student", tags=["student"], summary="create a student")
def student_create_api_view(request):
    pass


@router.get(
    "/student/{student_id}", tags=["student"], summary="git a particlar student"
)
def student_retrive_api_view(request):
    pass


@router.put(
    "/student/{student_id}",
    tags=["student"],
    summary="fully and partial update of a student",
)
def student_update_api_view(request):
    pass


@router.delete("/student/{student_id}", tags=["student"], summary="delete a student")
def student_destroy_api_view(request):
    pass
