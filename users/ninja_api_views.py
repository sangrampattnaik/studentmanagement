from .schemas import UserLoginSchema
from ninja import NinjaAPI
from auth.ninja_auth import Authorization
from django.contrib.auth import authenticate
from .backend import app


api = NinjaAPI(title="Student Management System",version="1.0.0",docs_url="swagger/",auth=Authorization())


@api.post('/login', tags=['user login'], summary="user login",auth=None)
def user_login(request, body: UserLoginSchema):
    response = app.authenticate_user(body)
    return response
    

@api.post('/forgot-password',tags=['user forgot password'],summary="reset user forgotten password")
def forgot_password(request):
    pass



@api.get('/teacher',tags=['teacher'],summary="get list of teachers")
def teacher_list_api_view(request):
    pass

@api.post('/teacher',tags=['teacher'],summary="create a teacher")
def teacher_create_api_view(request):
    pass

@api.get('/teacher/{teacher_id}',tags=['teacher'],summary="git a particlar teacher")
def teacher_retrive_api_view(request):
    pass
@api.put('/teacher/{teacher_id}',tags=['teacher'],summary="fully and partial update of a teacher")
def teacher_update_api_view(request):
    pass
@api.delete('/teacher/{teacher_id}',tags=['teacher'],summary="delete a teacher")
def teacher_destroy_api_view(request):
    pass


@api.get('/student',tags=['student'],summary="get list of students")
def student_list_api_view(request):
    pass

@api.post('/student',tags=['student'],summary="create a student")
def student_create_api_view(request):
    pass

@api.get('/student/{student_id}',tags=['student'],summary="git a particlar student")
def student_retrive_api_view(request):
    pass
@api.put('/student/{student_id}',tags=['student'],summary="fully and partial update of a student")
def student_update_api_view(request):
    pass
@api.delete('/student/{student_id}',tags=['student'],summary="delete a student")
def student_destroy_api_view(request):
    pass

# @api.get('/student')
# @api.post('/student')
# @api.get('/student/{student_id}')
# @api.put('/student/{student_id}')
# @api.patch('/student/{student_id}')
# @api.delete('/student/{student_id}')
