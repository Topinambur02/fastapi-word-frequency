from service.text_report_service import TextReportService
from dependencies.text_report_dependencies import get_text_report_service


def test_get_text_report_service_returns_correct_instance():
    """
    Проверяет, что провайдер зависимостей возвращает объект правильного типа.

    Убеждается, что результат вызова get_text_report_service является
    экземпляром класса TextReportService.
    """
    service = get_text_report_service()

    assert isinstance(service, TextReportService)


def test_get_text_report_service_creates_new_instance():
    """
    Проверяет, что провайдер не является синглтоном.

    Убеждается, что каждый вызов get_text_report_service возвращает
    новый уникальный экземпляр объекта (разные адреса в памяти).
    """
    service1 = get_text_report_service()
    service2 = get_text_report_service()

    assert service1 is not service2
