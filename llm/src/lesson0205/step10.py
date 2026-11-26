# https://stepik.org/lesson/2075470/step/10?unit=2104620

COLD_START_SECONDS = 1.0


def generation_speed(response: dict) -> dict:
    """
    Вычисляет метрики скорости генерации на основе ответа Ollama API.

    Args:
        response: Ответ /api/chat без потоковой передачи с ключами:
            - eval_count: токенов в ответе
            - eval_duration: время генерации в наносекундах
            - prompt_eval_count: токенов в промпте
            - prompt_eval_duration: время обработки промпта в наносекундах
            - load_duration: время загрузки модели в наносекундах
            - total_duration: полное время в наносекундах

    Returns:
        dict с ключами:
            - answer_tps: токенов ответа в секунду (округлено до 1 знака)
            - prompt_tps: токенов промпта в секунду (округлено до 1 знака)
            - total_seconds: полное время в секундах (округлено до 2 знаков)
            - cold_start: True если модель загружалась в память
    """
    # Извлекаем данные из ответа
    eval_count = response.get("eval_count", 0)
    eval_duration = response.get("eval_duration", 0)
    prompt_eval_count = response.get("prompt_eval_count", 0)
    prompt_eval_duration = response.get("prompt_eval_duration", 0)
    load_duration = response.get("load_duration", 0)
    total_duration = response.get("total_duration", 0)

    # Переводим наносекунды в секунды
    eval_duration_sec = eval_duration / 1_000_000_000
    prompt_eval_duration_sec = prompt_eval_duration / 1_000_000_000
    load_duration_sec = load_duration / 1_000_000_000
    total_duration_sec = total_duration / 1_000_000_000

    # Вычисляем скорости
    # Если время равно 0, скорость равна 0.0
    if eval_duration_sec > 0:
        answer_tps = round(eval_count / eval_duration_sec, 1)
    else:
        answer_tps = 0.0

    if prompt_eval_duration_sec > 0:
        prompt_tps = round(prompt_eval_count / prompt_eval_duration_sec, 1)
    else:
        prompt_tps = 0.0

    # Округляем полное время до 2 знаков
    total_seconds = round(total_duration_sec, 2)

    # Определяем холодный старт
    cold_start = load_duration_sec > COLD_START_SECONDS

    return {
        "answer_tps": answer_tps,
        "prompt_tps": prompt_tps,
        "total_seconds": total_seconds,
        "cold_start": cold_start
    }
