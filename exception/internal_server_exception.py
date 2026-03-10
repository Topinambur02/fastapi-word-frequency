from fastapi import status

from exception.base_exception import BaseException


class InternalServerException(BaseException):
    '''
    Исключение, выбрасываемое при внутренней ошибке сервера (500).

    Используется для обработки непредвиденных ситуаций на стороне сервера,
    когда выполнение запроса невозможно.
    '''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Internal server error'

    def __init__(self, detail=None):
        super().__init__(status_code=self.status_code, detail=detail)
