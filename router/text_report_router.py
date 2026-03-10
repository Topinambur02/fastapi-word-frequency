from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks

from service.text_report_service import TextReportService
from dependencies.text_report_dependencies import get_text_report_service


text_report_router = APIRouter()


@text_report_router.post('/export')
async def export_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    service: TextReportService = Depends(get_text_report_service),
):
    '''
    Эндпоинт для конвертации текстового отчета в формат Excel.

    Принимает текстовый файл, обрабатывает его содержимое в отдельном процессе 
    и возвращает сгенерированный файл .xlsx.

    Args:
        background_tasks (BackgroundTasks): Механизм FastAPI для выполнения 
            очистки временных файлов после отправки ответа.
        file (UploadFile): Загружаемый пользователем текстовый файл.
        service (TextReportService): Сервис для обработки бизнес-логики отчетов.

    Returns:
        FileResponse: Сгенерированный Excel-файл.

    Raises:
        BadRequestException: Если файл не был передан.
        InternalServerException: При ошибках во время обработки файла.
    '''
    return await service.export_report(file=file, background_tasks=background_tasks)
