from service.text_report_service import TextReportService


def get_text_report_service() -> TextReportService:
    """
    Инициализирует и возвращает экземпляр сервиса для работы с текстовыми отчетами.
    Используется в качестве Dependency Injection в веб-фреймворках.
    Returns:
        TextReportService: Экземпляр класса сервиса текстовых отчетов.
    """
    return TextReportService()
