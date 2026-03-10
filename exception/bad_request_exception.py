from fastapi import status

from exception.base_exception import BaseException


class BadRequestException(BaseException):
    """
    Исключение, выбрасываемое при ошибке 400 (Bad Request).

    Используется, когда клиент отправил некорректные данные или
    запрос не может быть обработан из-за семантических ошибок.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request"

    def __init__(self, detail=None):
        super().__init__(status_code=self.status_code, detail=detail)
