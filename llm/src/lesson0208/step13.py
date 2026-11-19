# https://stepik.org/lesson/2075624/step/13?unit=2104775

MODEL = "llama3.2:3b"
NUM_PREDICT = 512
SYSTEM_PROMPT = "You are a helpful assistant."


def build_chat_request(text: str, examples: list[tuple[str, str]], schema: dict) -> dict:
    """
    Собирает тело запроса к /api/chat Ollama с инструкцией, примерами и JSON-схемой.

    Args:
        text: str - текст, который модель должна обработать
        examples: list[tuple[str, str]] - примеры: пары (текст, ответ модели)
        schema: dict - JSON-схема ответа

    Returns:
        dict: тело запроса с полями model, messages, format, stream, think, options
    """
    # Формируем список сообщений
    messages = []

    # Первое сообщение - system
    messages.append({"role": "system", "content": SYSTEM_PROMPT})

    # Добавляем примеры: каждый пример превращается в два сообщения (user и assistant)
    for example_text, example_response in examples:
        messages.append({"role": "user", "content": example_text})
        messages.append({"role": "assistant", "content": example_response})

    # Последнее сообщение - user с текстом без пробелов по краям
    messages.append({"role": "user", "content": text.strip()})

    # Формируем тело запроса
    return {
        "model": MODEL,
        "messages": messages,
        "format": schema,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0,
            "num_predict": NUM_PREDICT
        }
    }
