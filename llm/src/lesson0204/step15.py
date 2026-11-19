# https://stepik.org/lesson/2075437/step/15?unit=2104588

from openai import OpenAI, RateLimitError, OpenAIError

MAX_TOKENS = 1024


def ask_free(client: OpenAI, question: str, models: list[str]) -> tuple[str, str]:
    """
    Отправляет вопрос бесплатным моделям OpenRouter по очереди.
    Переходит к следующей модели при превышении лимита.

    Args:
        client: OpenAI - клиент OpenRouter
        question: str - вопрос пользователя
        models: list[str] - имена бесплатных моделей в порядке приоритета

    Returns:
        tuple[str, str] - имя модели, которая ответила, и текст ответа без пробелов по краям

    Raises:
        RateLimitError: если все модели ответили превышением лимита
        OpenAIError: при других ошибках API
    """
    last_rate_limit_error = None

    for model in models:
        try:
            # Вызываем API OpenRouter через OpenAI клиент
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": question}],
                max_tokens=MAX_TOKENS,
                reasoning_effort="none"
            )
            # Успешный ответ - возвращаем имя модели и текст ответа
            answer_text = response.choices[0].message.content.strip()
            return (model, answer_text)

        except RateLimitError as e:
            # Сохраняем ошибку и пробуем следующую модель
            last_rate_limit_error = e
            continue

        except OpenAIError:
            # Другая ошибка OpenAI - выбрасываем сразу
            raise

    # Если все модели ответили RateLimitError, выбрасываем последнюю ошибку
    if last_rate_limit_error is not None:
        raise last_rate_limit_error
