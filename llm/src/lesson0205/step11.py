# https://stepik.org/lesson/2075470/step/11?unit=2104620

import re


def parse_ollama_ps(output: str) -> list:
    """
    Разбирает текстовый вывод команды ollama ps в список моделей.

    Args:
        output: Вывод ollama ps со строкой заголовка и строками моделей.
                Колонки NAME, ID, SIZE, PROCESSOR, CONTEXT, UNTIL разделены
                двумя и более пробелами.

    Returns:
        Список словарей с ключами:
            - name: имя модели из колонки NAME
            - size_gb: память из SIZE в гигабайтах (округлено до 2 знаков)
            - context: окно контекста из CONTEXT
            - full_gpu: True если PROCESSOR равен "100% GPU"
    """
    result = []
    lines = output.strip().split('\n')

    # Пропускаем заголовок (первую строку)
    for i, line in enumerate(lines):
        if i == 0:  # Пропускаем заголовок
            continue

        # Пропускаем пустые строки
        if not line.strip():
            continue

        # Разбиваем по двум и более пробелам
        columns = re.split(r'\s{2,}', line.strip())

        # Должно быть минимум 5 колонок (NAME, ID, SIZE, PROCESSOR, CONTEXT)
        if len(columns) < 5:
            continue

        name = columns[0]
        size_str = columns[2]
        processor = columns[3]
        context_str = columns[4]

        # Парсим SIZE
        size_parts = size_str.split()
        if len(size_parts) >= 2:
            size_value = float(size_parts[0])
            size_unit = size_parts[1]

            if size_unit == 'GB':
                size_gb = size_value
            elif size_unit == 'MB':
                size_gb = size_value / 1000
            else:
                size_gb = size_value

            size_gb = round(size_gb, 2)
        else:
            size_gb = 0.0

        # Парсим CONTEXT
        context = int(context_str)

        # Проверяем PROCESSOR
        full_gpu = (processor == "100% GPU")

        result.append({
            "name": name,
            "size_gb": size_gb,
            "context": context,
            "full_gpu": full_gpu
        })

    return result
