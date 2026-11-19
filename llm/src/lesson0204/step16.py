# https://stepik.org/lesson/2075437/step/16?unit=2104588

def usage_cost(usage: dict, input_rate: float, output_rate: float) -> float:
    """
    Вычисляет стоимость запроса по числу входных и выходных токенов.

    Args:
        usage: dict - словарь с полями prompt_tokens и completion_tokens
        input_rate: float - стоимость миллиона входных токенов
        output_rate: float - стоимость миллиона выходных токенов

    Returns:
        float - стоимость запроса
    """
    # Извлекаем количество токенов
    prompt_tokens = usage["prompt_tokens"]
    completion_tokens = usage["completion_tokens"]

    # Рассчитываем стоимость входных токенов
    input_cost = prompt_tokens * input_rate / 1_000_000

    # Рассчитываем стоимость выходных токенов
    output_cost = completion_tokens * output_rate / 1_000_000

    # Возвращаем общую стоимость
    return input_cost + output_cost
