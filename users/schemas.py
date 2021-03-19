from ninja import Schema

class UserLoginSchema(Schema):
    username:str
    password:str