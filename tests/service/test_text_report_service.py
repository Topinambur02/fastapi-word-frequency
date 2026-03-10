import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile

from service.text_report_service import TextReportService
from exception.bad_request_exception import BadRequestException
from exception.internal_server_exception import InternalServerException


@pytest.mark.asyncio
class TestTextReportService:
    async def test_export_report_success(self, service, mock_upload_file, mock_background_tasks):
        """Проверка успешного сценария обработки файла."""
        
        with patch("tempfile.mkstemp") as mock_mkstemp, \
            patch("os.close"), \
            patch("aiofiles.open", MagicMock()) as _, \
            patch("asyncio.get_running_loop") as mock_loop:

            mock_mkstemp.side_effect = [(1, "in.txt"), (2, "out.xlsx")]
            
            mock_loop_instance = MagicMock()
            mock_loop_instance.run_in_executor = AsyncMock()
            mock_loop.return_value = mock_loop_instance

            response = await service.export_report(
                file=mock_upload_file, 
                background_tasks=mock_background_tasks
            )

            assert response.path == "out.xlsx"
            assert "report_test_report.txt.xlsx" in response.filename
            
            mock_loop_instance.run_in_executor.assert_called_once()
            
            mock_background_tasks.add_task.assert_called_once()

    async def test_export_report_no_filename(self, service, mock_background_tasks):
        """Проверка ошибки, если файл без имени."""

        mock_file = MagicMock(spec=UploadFile)
        mock_file.filename = None

        with pytest.raises(BadRequestException) as exc:
            await service.export_report(file=mock_file, background_tasks=mock_background_tasks)
        
        assert "The file was not transferred" in str(exc.value.detail)

    async def test_export_report_internal_error(self, service, mock_upload_file, mock_background_tasks):
        """Проверка обработки внутренних ошибок и вызова очистки."""
        
        with patch("tempfile.mkstemp", return_value=(1, "temp.path")), \
            patch("os.close"), \
            patch("aiofiles.open", side_effect=Exception("Disk full")):

            with pytest.raises(InternalServerException) as exc:
                await service.export_report(file=mock_upload_file, background_tasks=mock_background_tasks)

            assert "File processing error" in str(exc.value.detail)

    async def test_init_pool_size(self):
        """Проверка корректной инициализации пула процессов."""

        with patch("os.cpu_count", return_value=4):
            svc = TextReportService()

            assert svc.process_pool._max_workers == 4