# https://stepik.org/lesson/2075624/step/16?unit=2104775

import re


def extract_answer(response: dict) -> int | None:
    """
    Извлекает итоговое число из ответа модели, рассуждавшей по шагам.

    Args:
        response: dict - ответ /api/chat Ollama с ключами message и done_reason

    Returns:
        int | None - итоговое число или None, если ответа нет или он обрезан
    """
    # Проверка 1: Если ответ обрезан, вернуть None
    if response.get("done_reason") == "length":
        return None

    # Получаем текст ответа
    try:
        content = response["message"]["content"]
    except (KeyError, TypeError):
        return None

    # Разбиваем текст на строки
    lines = content.split('\n')

    # Находим последнюю непустую строку
    last_nonempty_line = None
    for line in lines:
        if line.strip():  # Если строка не пустая после удаления пробелов
            last_nonempty_line = line

    # Если нет непустых строк
    if last_nonempty_line is None:
        return None

    # Убираем пробелы по краям
    last_line = last_nonempty_line.strip()

    # Проверяем формат строки: "Ответ:" + пробелы + число (возможно со знаком минус) + пробелы
    # Используем регулярное выражение для проверки формата
    pattern = r'^Ответ:\s*(-?\d+)\s*$'
    match = re.match(pattern, last_line)

    if match:
        # Извлекаем число и возвращаем как int
        return int(match.group(1))

    # Если формат не подходит
    return None
