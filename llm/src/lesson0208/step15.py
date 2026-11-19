# https://stepik.org/lesson/2075624/step/15?unit=2104775

def fit_history(
        system: str,
        history: list[dict],
        question: str,
        num_ctx: int,
        num_predict: int
) -> list[dict]:
    """
    Собирает сообщения запроса и удаляет самые старые пары из истории,
    пока промпт вместе с лимитом ответа не поместится в окно контекста.

    Args:
        system: str - текст системного сообщения
        history: list[dict] - прошлые сообщения диалога (пары user/assistant от старых к новым)
        question: str - новый вопрос пользователя
        num_ctx: int - размер окна контекста в токенах
        num_predict: int - лимит токенов ответа

    Returns:
        list[dict]: сообщения запроса (system, история, question)

    Raises:
        ValueError: если запрос не помещается даже без истории
    """
    # Создаем копию истории, чтобы не изменять оригинал
    working_history = history[:]

    while True:
        # Формируем список сообщений запроса
        messages = [{"role": "system", "content": system}]
        messages.extend(working_history)
        messages.append({"role": "user", "content": question})

        # Вычисляем размер промпта
        prompt_size = sum(count_tokens(msg["content"]) for msg in messages)

        # Проверяем, помещается ли запрос
        if prompt_size + num_predict <= num_ctx:
            return messages

        # Если история пустая и запрос не помещается, выбрасываем ошибку
        if len(working_history) == 0:
            raise ValueError()

        # Удаляем самую старую пару (user и assistant)
        working_history = working_history[2:]
