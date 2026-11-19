# https://stepik.org/lesson/2075122/step/13?unit=2104233

import json

MAX_SUMMARY = 100


def read_label(response: dict, categories: set[str]) -> dict:
    # Проверка 1: Если done_reason равен "length", верните статус "truncated"
    if response.get("done_reason") == "length":
        return {
            "status": "truncated",
            "category": None,
            "summary": None
        }

    # Получаем текст ответа модели
    try:
        content = response["message"]["content"]
    except (KeyError, TypeError):
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    # Проверка 2: Разбираем текст ответа как JSON
    try:
        parsed = json.loads(content)
        # Проверяем, что это объект JSON (словарь)
        if not isinstance(parsed, dict):
            return {
                "status": "invalid",
                "category": None,
                "summary": None
            }
    except (json.JSONDecodeError, TypeError):
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    # Проверка 3: Проверяем корректность объекта
    # Проверяем наличие ключей "category" и "summary"
    if "category" not in parsed or "summary" not in parsed:
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    category = parsed["category"]
    summary = parsed["summary"]

    # Проверяем, что оба значения - строки
    if not isinstance(category, str) or not isinstance(summary, str):
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    # Проверяем, что категория входит в categories
    if category not in categories:
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    # Проверяем, что описание не длиннее MAX_SUMMARY символов
    if len(summary) > MAX_SUMMARY:
        return {
            "status": "invalid",
            "category": None,
            "summary": None
        }

    # Все проверки пройдены
    return {
        "status": "ok",
        "category": category,
        "summary": summary
    }
