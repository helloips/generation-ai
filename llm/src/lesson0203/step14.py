# https://stepik.org/lesson/2075217/step/14?unit=2104339

import re

SYSTEM_PROMPT = "You are a helpful customer support assistant."


def normalize_question(question: str) -> str:
    """Нормализует вопрос: удаляет пробелы по краям, приводит к нижнему регистру,
    заменяет несколько пробелов подряд на один."""
    # Удаляем пробелы по краям и приводим к нижнему регистру
    normalized = question.strip().lower()
    # Заменяем несколько пробелов подряд на один
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized


async def answer_all(llm, questions: list[str], cache: dict[str, str]) -> list[str]:
    """Отвечает на вопросы клиентов через модель, используя кэш для избежания повторных вызовов."""
    answers = []

    for question in questions:
        # Нормализуем вопрос для поиска в кэше
        normalized = normalize_question(question)

        # Проверяем, есть ли ответ в кэше
        if normalized in cache:
            # Берем ответ из кэша
            answers.append(cache[normalized])
        else:
            # Вызываем модель
            # Используем исходный вопрос без пробелов по краям для запроса к модели
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question.strip()}
            ]
            answer = await llm.generate(messages)

            # Сохраняем ответ в кэш по нормализованному вопросу
            cache[normalized] = answer
            answers.append(answer)

    return answers
