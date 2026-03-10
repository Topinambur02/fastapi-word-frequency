import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app


@pytest.mark.asyncio
async def test_export_report_success(mock_service):
    """
    Проверка успешной загрузки файла и вызова метода сервиса.
    """
    mock_service.export_report.return_value = {"status": "success"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("test.txt", b"some content", "text/plain")}
        response = await ac.post("/public/report/export", files=files)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_export_report_no_file():
    """
    Проверка ошибки, если файл не передан.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/public/report/export")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
