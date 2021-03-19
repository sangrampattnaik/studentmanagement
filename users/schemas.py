from ninja import Schema


class UserLoginSchema(Schema):
    username: str
    password: str


class UserSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

class UserUpdateSchema(Schema):
    username: str = None
    email: str = None
    first_name: str = None
    last_name: str = None


class PageSizeQuerySchema(Schema):
    page: int = 1
    size: int = 20
