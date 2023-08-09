from fastapi import HTTPException, status


class CustomExeptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(CustomExeptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class NotUserExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Нет такого пользователя или пароль введен неверно"


class FieldTokenExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Field Token"


class FieldExpirationExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Field expiration Token"


class NotUIDExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "UID not found in token"


class NotUIDinDBExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "UID not found in db"


class NotAdminExeption(CustomExeptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "ТЫ НЕ АДМИН!!!"


class NotVolExeption(CustomExeptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нет vol для данного ticker"
