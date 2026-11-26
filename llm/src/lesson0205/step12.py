# https://stepik.org/lesson/2075470/step/12?unit=2104620

CONTEXT_MARGIN = 100


def check_responses(calls: list[dict]) -> dict:
    """
    Анализирует ответы Ollama и определяет вердикт для каждого запроса.

    Args:
        calls: Список запросов к модели. Каждый запрос содержит:
            - id: идентификатор запроса
            - num_ctx: окно контекста в запросе
            - response: ответ /api/chat с ключами:
                - prompt_eval_count: число обработанных токенов
                - done_reason: причина завершения генерации

    Returns:
        dict с ключами:
            - verdicts: словарь {id_запроса: вердикт}
            - totals: словарь с подсчетом каждого типа вердикта
    """
    verdicts = {}
    totals = {
        "ok": 0,
        "near_context_limit": 0,
        "answer_truncated": 0
    }

    for call in calls:
        request_id = call["id"]
        num_ctx = call["num_ctx"]
        response = call["response"]

        prompt_eval_count = response.get("prompt_eval_count", 0)
        done_reason = response.get("done_reason", "")

        # Проверяем условия в указанном порядке
        # 1. Окно контекста близко к заполнению
        if prompt_eval_count >= num_ctx - CONTEXT_MARGIN:
            verdict = "near_context_limit"
        # 2. Ответ обрезан по лимиту длины
        elif done_reason == "length":
            verdict = "answer_truncated"
        # 3. Иначе все в порядке
        else:
            verdict = "ok"

        verdicts[request_id] = verdict
        totals[verdict] += 1

    return {
        "verdicts": verdicts,
        "totals": totals
    }
