from concurrent.futures import ProcessPoolExecutor
from fastapi import UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

from exception.bad_request_exception import BadRequestException
from exception.internal_server_exception import InternalServerException
from utils.cleanup_files import cleanup_files
from utils.process_file_task import process_file_task

import os
import tempfile
import asyncio
import aiofiles


class TextReportService:
    """
    Сервис для высокопроизводительной обработки текстовых отчетов.

    Использует пул процессов для выполнения ресурсоемких задач (CPU-bound),
    чтобы избежать блокировки асинхронного цикла событий приложения.

    Attributes:
        process_pool (ProcessPoolExecutor): Пул процессов для параллельной обработки.
    """

    def __init__(self):
        self.process_pool = ProcessPoolExecutor(max_workers=os.cpu_count())

    async def export_report(
        self, *, file: UploadFile, background_tasks: BackgroundTasks
    ):
        """
        Обрабатывает загруженный файл и конвертирует его в Excel.

        Метод выполняет следующие шаги:
        1. Создает временные файлы для входных и выходных данных.
        2. Асинхронно сохраняет поток загруженного файла на диск.
        3. Запускает задачу обработки в `ProcessPoolExecutor`.
        4. Регистрирует задачу очистки временных файлов.
        5. Возвращает файл пользователю.

        Args:
            file (UploadFile): Объект загруженного файла.
            background_tasks (BackgroundTasks): Задачи для выполнения после ответа.

        Returns:
            FileResponse: Путь к готовому Excel-файлу с метаданными.

        Raises:
            BadRequestException: Если имя файла отсутствует.
            InternalServerException: Если в процессе обработки возникло исключение.
        """
        if not file.filename:
            raise BadRequestException(detail="The file was not transferred")

        fd_in, temp_input_path = tempfile.mkstemp(suffix=".txt")
        fd_out, temp_output_path = tempfile.mkstemp(suffix=".xlsx")

        os.close(fd_in)
        os.close(fd_out)

        try:
            async with aiofiles.open(temp_input_path, "wb") as buffer:
                while chunk := await file.read(1024 * 1024 * 10):
                    await buffer.write(chunk)

            loop = asyncio.get_running_loop()

            await loop.run_in_executor(
                self.process_pool, process_file_task, temp_input_path, temp_output_path
            )

            background_tasks.add_task(cleanup_files, temp_input_path, temp_output_path)

            return FileResponse(
                path=temp_output_path,
                filename=f"report_{file.filename}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        except Exception as e:
            cleanup_files(temp_input_path, temp_output_path)
            raise InternalServerException(detail=f"File processing error: {str(e)}")
