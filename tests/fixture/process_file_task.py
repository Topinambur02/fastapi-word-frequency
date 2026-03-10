import pytest


@pytest.fixture
def temp_files(tmp_path):
    """
    Фикстура для создания временных путей входного и выходного файлов.
    """
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.xlsx"
    return input_file, output_file
