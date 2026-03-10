from fastapi import status, HTTPException

from exception.bad_request_exception import BadRequestException
from exception.internal_server_exception import InternalServerException


def test_bad_request_exception_defaults():
    exc = BadRequestException()

    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.detail == "Bad request"


def test_exception_custom_detail():
    custom_msg = "Invalid email format"
    exc = BadRequestException(detail=custom_msg)

    assert exc.detail == custom_msg
    assert exc.status_code == status.HTTP_400_BAD_REQUEST


def test_internal_server_exception_inheritance():
    exc = InternalServerException()

    assert isinstance(exc, HTTPException)
