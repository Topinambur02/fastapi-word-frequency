import os
import pandas as pd

from utils.process_file_task import process_file_task


def test_process_file_basic_logic(temp_files):
    """
    Проверяет базовую логику: корректность лемматизации, подсчет общего
    количества слов и генерацию выходного файла.
    """
    input_path, output_path = temp_files
    content = "Бежал кот.\nКот хочет бежать."
    input_path.write_text(content, encoding="utf-8")

    process_file_task(str(input_path), str(output_path))

    assert os.path.exists(output_path)
    df = pd.read_excel(output_path)

    cat_row = df[df["Словоформа"] == "кот"]
    assert cat_row["Кол-во во всём документе"].iloc[0] == 2

    run_row = df[df["Словоформа"] == "бежать"]
    assert run_row["Кол-во во всём документе"].iloc[0] == 2


def test_process_file_line_statistics(temp_files):
    """
    Проверяет корректность формирования строки с распределением слов по строкам (column index 2).
    Убеждается, что индексы строк соответствуют количеству вхождений.
    """
    input_path, output_path = temp_files
    content = "Мама\nмыла\nмама"
    input_path.write_text(content, encoding="utf-8")

    process_file_task(str(input_path), str(output_path))

    df = pd.read_excel(output_path)
    mama_stats = df[df["Словоформа"] == "мама"]["Кол-во в каждой из строк"].iloc[0]

    assert mama_stats == "1,0,1"


def test_process_file_empty_input(temp_files):
    """
    Проверяет поведение функции при пустом входном файле.
    Файл должен создаться только с заголовками.
    """
    input_path, output_path = temp_files
    input_path.write_text("", encoding="utf-8")

    process_file_task(str(input_path), str(output_path))

    df = pd.read_excel(output_path)
    assert len(df) == 0


def test_process_file_mixed_languages_and_trash(temp_files):
    """
    Проверяет, что регулярное выражение корректно фильтрует знаки препинания
    и обрабатывает смесь кириллицы и латиницы.
    """
    input_path, output_path = temp_files
    content = "Hello, мир! 123 @#$ Hello."
    input_path.write_text(content, encoding="utf-8")

    process_file_task(str(input_path), str(output_path))

    df = pd.read_excel(output_path)
    hello_row = df[df["Словоформа"] == "hello"]

    assert hello_row["Кол-во во всём документе"].iloc[0] == 2
    assert "123" not in df["Словоформа"].values
