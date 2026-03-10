import pytest
from unittest.mock import MagicMock

from tests.fixture.text_report_router import mock_service
from tests.fixture.text_report_service import mock_upload_file
from tests.fixture.text_report_service import mock_background_tasks
from tests.fixture.text_report_service import service
from tests.fixture.process_file_task import temp_files
