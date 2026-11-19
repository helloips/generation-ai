# https://stepik.org/lesson/2075624/step/14?unit=2104775

def to_ollama_body(request: dict) -> dict:
    """
    Переводит тело запроса в формате OpenAI API в формат Ollama API.

    Args:
        request: dict - тело запроса в формате OpenAI API

    Returns:
        dict: тело запроса в формате Ollama API

    Raises:
        ValueError: если в request есть недопустимый ключ
    """
    # Допустимые ключи
    allowed_keys = {"model", "messages", "stream", "temperature", "max_tokens", "stop", "seed", "reasoning_effort"}

    # Проверяем наличие недопустимых ключей
    for key in request:
        if key not in allowed_keys:
            raise ValueError(key)

    # Формируем результат
    result = {
        "model": request["model"],
        "messages": request["messages"],
        "stream": request.get("stream", False)
    }

    # Таблица соответствия параметров генерации
    param_mapping = {
        "temperature": "temperature",
        "max_tokens": "num_predict",
        "stop": "stop",
        "seed": "seed"
    }

    # Формируем options
    options = {}
    for openai_param, ollama_param in param_mapping.items():
        if openai_param in request:
            options[ollama_param] = request[openai_param]

    result["options"] = options

    # Обрабатываем reasoning_effort
    if "reasoning_effort" in request:
        result["think"] = request["reasoning_effort"] != "none"

    return result
