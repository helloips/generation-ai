# https://stepik.org/lesson/2075437/step/13?unit=2104588

MODEL = "mistral-small-latest"
MAX_TOKENS = 1024
SYSTEM_PROMPT = "You are a helpful assistant."


def ask_mistral(client, question: str) -> dict:
    """
    Отправляет вопрос модели Mistral и возвращает текст ответа с расходом токенов.

    Args:
        client: Mistral - клиент Mistral API
        question: str - вопрос пользователя

    Returns:
        dict: {"text": str, "tokens": int}

    Raises:
        ValueError: если ответ обрезан (finish_reason == "length")
    """
    # Формируем список сообщений
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question.strip()}
    ]

    # Вызываем API Mistral
    response = client.chat.complete(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=messages
    )

    # Проверяем первый вариант ответа
    first_choice = response.choices[0]

    # Проверяем, обрезан ли ответ
    if first_choice.finish_reason == "length":
        raise ValueError("Response was truncated")

    # Извлекаем текст ответа
    answer_text = first_choice.message.content.strip()

    # Вычисляем общее количество токенов
    total_tokens = response.usage.prompt_tokens + response.usage.completion_tokens

    return {
        "text": answer_text,
        "tokens": total_tokens
    }
