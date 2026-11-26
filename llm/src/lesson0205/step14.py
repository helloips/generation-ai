# https://stepik.org/lesson/2075470/step/14?unit=2104620


def release_model(runtime, model: str, prompts: list[str]) -> list[str]:
    """
    Выполняет серию запросов к модели и освобождает память после завершения.

    Args:
        runtime: InferenceRuntime объект для генерации ответов и выгрузки модели
        model: точное имя модели
        prompts: список текстов запросов в исходном порядке

    Returns:
        Список ответов модели в порядке запросов

    Raises:
        Любые исключения от runtime.generate передаются дальше после выгрузки модели
    """
    responses = []
    try:
        # Обрабатываем каждый промпт по порядку
        for prompt in prompts:
            response = runtime.generate(model, prompt)
            responses.append(response)
        return responses
    finally:
        # Гарантируем вызов unload ровно один раз в любом случае:
        # - после успешной обработки всех промптов
        # - при пустом списке промптов
        # - при ошибке генерации
        runtime.unload(model)
