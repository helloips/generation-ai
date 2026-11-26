# https://stepik.org/lesson/2075470/step/13?unit=2104620

import json


def collect_stream(lines: list[str]) -> dict:
    """
    Собирает ответ модели из строк потока REST API Ollama.

    Args:
        lines: Список строк потока /api/chat. Каждая строка — JSON-объект с:
            - message: словарь с ключами content и иногда thinking
            - done: булево значение, True в последней части
            В последней части также есть done_reason и eval_count

    Returns:
        dict с ключами:
            - content: текст ответа, склеенный из всех частей
            - thinking: рассуждение, склеенное из всех частей, или пустая строка
            - done_reason: причина остановки из последней части
            - eval_count: число токенов из последней части

    Raises:
        ValueError: если поток оборвался (нет части с "done": true)
    """
    content_parts = []
    thinking_parts = []
    done_reason = None
    eval_count = None
    stream_completed = False

    for line in lines:
        # Пропускаем пустые строки
        if not line.strip():
            continue

        # Разбираем JSON
        try:
            part = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Извлекаем message
        message = part.get("message", {})

        # Собираем content
        if "content" in message:
            content_parts.append(message["content"])

        # Собираем thinking
        if "thinking" in message:
            thinking_parts.append(message["thinking"])

        # Проверяем, завершен ли поток
        if part.get("done", False):
            stream_completed = True
            done_reason = part.get("done_reason", "")
            eval_count = part.get("eval_count", 0)

    # Если поток не завершен, выбрасываем ошибку
    if not stream_completed:
        raise ValueError("поток оборвался")

    return {
        "content": "".join(content_parts),
        "thinking": "".join(thinking_parts),
        "done_reason": done_reason,
        "eval_count": eval_count
    }
