import os
import pytest

from utils.cleanup_files import cleanup_files


def test_cleanup_existing_files(tmp_path):
    """
    Проверяет успешное удаление нескольких существующих временных файлов.
    
    Создает реальные файлы в изолированной временной директории и 
    подтверждает, что после вызова функции файлы физически отсутствуют.
    """
    file1 = tmp_path / "test1.txt"
    file2 = tmp_path / "test2.txt"
    file1.write_text("content")
    file2.write_text("content")

    cleanup_files(str(file1), str(file2))

    assert not os.path.exists(file1)
    assert not os.path.exists(file2)


def test_cleanup_non_existent_file():
    """
    Проверяет устойчивость функции к отсутствующим путям.
    
    Тест проходит успешно, если функция корректно обрабатывает ситуацию, 
    когда файла не существует, не вызывая исключений (краша программы).
    """
    path = "non_existent_file.tmp"
    
    try:
        cleanup_files(path)
    except Exception as e:
        pytest.fail(f"cleanup_files raised an exception on missing file: {e}")


def test_cleanup_mixed_files(tmp_path):
    """
    Проверяет работу функции в смешанном сценарии (существующие и нет файлы).
    
    Гарантирует, что наличие одного несуществующего пути не прерывает 
    процесс удаления других файлов, переданных в аргументах.
    """
    existing = tmp_path / "exists.txt"
    existing.write_text("data")
    missing = tmp_path / "missing.txt"

    cleanup_files(str(existing), str(missing))

    assert not os.path.exists(existing)


def test_cleanup_permission_error(tmp_path, capsys):
    """
    Проверяет обработку системных ошибок при попытке удаления.
    
    Имитирует ошибку (попытка удалить директорию через os.remove) и 
    проверяет, что блок try/except перехватывает её и выводит 
    соответствующее сообщение в консоль.
    """
    test_file = tmp_path / "protected.txt"
    test_file.write_text("data")
    
    dir_path = tmp_path / "some_dir"
    dir_path.mkdir()

    cleanup_files(str(dir_path))

    captured = capsys.readouterr()

    assert "Error when deleting a file" in captured.out