import pytest

from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile, BackgroundTasks

from service.text_report_service import TextReportService


@pytest.fixture
def service():
    with patch("os.cpu_count", return_value=2):
        return TextReportService()


@pytest.fixture
def mock_upload_file():
    file = MagicMock(spec=UploadFile)
    file.filename = "test_report.txt"
    file.read = AsyncMock(side_effect=[b"chunk1", b"chunk2", b""])
    return file


@pytest.fixture
def mock_background_tasks():
    return MagicMock(spec=BackgroundTasks)
