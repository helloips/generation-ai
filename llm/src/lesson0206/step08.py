# https://stepik.org/lesson/2085242/step/8?unit=2115513

def complete_base(runtime, model: str, prompt: str, stops: list[str]) -> str:
    """
    Отправляет base-модели текст для продолжения без шаблона чата.

    Args:
        runtime: CompletionClient - клиент для продолжения текста моделью
        model: str - точное имя модели
        prompt: str - текст для продолжения
        stops: list[str] - строки остановки генерации

    Returns:
        str - продолжение текста из поля response ответа модели
    """
    # Вызываем метод generate с указанными параметрами
    result = runtime.generate(
        model=model,
        prompt=prompt,
        raw=True,
        stream=False,
        options={"stop": stops}
    )

    # Возвращаем поле response без изменений
    return result["response"]
