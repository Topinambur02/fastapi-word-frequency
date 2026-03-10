import pytest
from unittest.mock import MagicMock, AsyncMock

from service.text_report_service import TextReportService
from dependencies.text_report_dependencies import get_text_report_service


@pytest.fixture(scope="function")
def mock_service():
    service = MagicMock(spec=TextReportService)
    service.export_report = AsyncMock()
    return service


@pytest.fixture(autouse=True, scope="function")
def override_dependency(app, mock_service):
    app.dependency_overrides[get_text_report_service] = lambda: mock_service
    yield
    app.dependency_overrides.clear()
