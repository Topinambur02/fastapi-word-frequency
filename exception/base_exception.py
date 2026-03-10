from fastapi import HTTPException, status


class BaseException(HTTPException):
    '''
    Базовый класс исключений для приложения.

    Наследуется от `HTTPException` и служит фундаментом для всех кастомных 
    ошибок API, обеспечивая стандартную структуру ответа.

    Attributes:
        status_code (int): HTTP статус-код (по умолчанию 500).
        detail (str): Краткое описание ошибки.
    '''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Something goes wrong'

    def __init__(self, status_code: int = None, detail: str = None):
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail
        
        super().__init__(status_code=self.status_code, detail=self.detail)
        