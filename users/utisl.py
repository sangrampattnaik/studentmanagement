def get_token(self, person):
        if person.is_active:
            if person.status == "Approved":
                if person.role_id.role_id in [1, 2, 5, 6]:
                    serializer = SuperAdminTutorSerializer
                elif person.role_id.role_id in [3, 7]:
                    serializer = TutorSerializer
                else:
                    serializer = StudentSerializer
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
            elif person.status == "Pending":
                raise AuthenticationFailed("kindly wait for approval")
            elif person.status == "Discarded":
                raise AuthenticationFailed(
                    "your account has been discarded. kindly contact admin to activate your account"
                )

            else:
                raise AuthenticationFailed("kindly wait for approval")
        else:
            raise AuthenticationFailed("kindly activate your account")




def authenticate(self, header_data=None, login_with_otp=False, person=None):
        try:
            if login_with_otp == False:
                prefix, encoded_data = header_data.split()
                if prefix == settings.JWT_AUTH["JWT_AUTHENTICATION_PREFIX"]:
                    username, password = get_username_password(encoded_data)
                if "@" in username:
                    person = Person.objects.filter(email=username)
                elif username.isdigit() and len(username) == 10:
                    person = Person.objects.filter(mobile_number=username)
                else:
                    person = Person.objects.filter(school_code=username)
            if len(person) == 1:
                person = person.first()
                if login_with_otp:
                    person.login_otp = ""
                    person.save()
                    self.get_token(person)
                    return self.token, self.person_serialized_data
                else:
                    if check_password(password, person.password):
                        self.get_token(person)
                        return self.token, self.person_serialized_data
                    else:
                        raise AuthenticationFailed("wrong password")
            else:
                raise AuthenticationFailed("wrong email or mobile or school code")
        except ValueError:
            raise AuthenticationFailed("authentication failed")