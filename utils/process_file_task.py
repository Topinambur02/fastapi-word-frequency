from pymorphy3 import MorphAnalyzer
from xlsxwriter.workbook import Workbook
from collections import defaultdict

import re


def process_file_task(input_filepath: str, output_filepath: str) -> None:
    """
    Изолированная функция для обработки файла.
    Выполняется в отдельном процессе, чтобы не блокировать GIL основного приложения FastAPI.
    """
    morph = MorphAnalyzer()
    lemma_cache = {}
    stats = defaultdict(lambda: {"total": 0, "lines": {}})
    total_lines = 0
    word_pattern = re.compile(r"[а-яА-ЯёЁa-zA-Z]+")

    with open(input_filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line_idx, line in enumerate(f):
            total_lines += 1
            words = word_pattern.findall(line.lower())

            for word in words:
                if word not in lemma_cache:
                    lemma_cache[word] = morph.parse(word)[0].normal_form

                lemma = lemma_cache[word]
                stats[lemma]["total"] += 1

                stats[lemma]["lines"][line_idx] = (
                    stats[lemma]["lines"].get(line_idx, 0) + 1
                )

    workbook = Workbook(output_filepath, {"constant_memory": True})
    worksheet = workbook.add_worksheet("Statistics")
    worksheet.write_row(
        0, 0, ["Словоформа", "Кол-во во всём документе", "Кол-во в каждой из строк"]
    )
    row_idx = 1

    for lemma, data in stats.items():
        total_count = data["total"]
        lines_data = data["lines"]

        line_counts_str = ",".join(
            str(lines_data.get(i, 0)) for i in range(total_lines)
        )

        worksheet.write_row(row_idx, 0, [lemma, total_count, line_counts_str])
        row_idx += 1

    workbook.close()
