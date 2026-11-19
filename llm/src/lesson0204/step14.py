# https://stepik.org/lesson/2075437/step/14?unit=2104588

import time
from mistralai import Mistral, MistralError

MODEL = "mistral-small-latest"
MAX_TOKENS = 1024


def ask_with_retry(
    client,
    messages: list[dict],
    attempts: int = 3,
    delay: float = 1.0,
    sleep=time.sleep
) -> str:
    """
    Отправляет запрос к Mistral API с повторами при ошибке 429 (превышение лимита).

    Args:
        client: Mistral - клиент Mistral API
        messages: list[dict] - сообщения запроса
        attempts: int - наибольшее число запросов к API (по умолчанию 3)
        delay: float - пауза перед повтором в секундах (по умолчанию 1.0)
        sleep: функция паузы (по умолчанию time.sleep)

    Returns:
        str - текст ответа модели без пробелов по краям

    Raises:
        MistralError: при ошибках API (429 на последней попытке или другой код)
    """
    for attempt in range(attempts):
        try:
            # Вызываем API Mistral
            response = client.chat.complete(
                model=MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            # Успешный вызов - возвращаем текст ответа
            return response.choices[0].message.content.strip()

        except MistralError as e:
            # Проверяем код ошибки
            if e.status_code == 429:
                # Ошибка превышения лимита
                if attempt < attempts - 1:
                    # Не последняя попытка - делаем паузу и повторяем
                    sleep(delay)
                    continue
                else:
                    # Последняя попытка - выбрасываем ошибку без паузы
                    raise
            else:
                # Другой код ошибки - выбрасываем сразу без паузы и повторов
                raise
