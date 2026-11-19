# https://stepik.org/lesson/2075122/step/14?unit=2104233

MAX_TEMPERATURE = 2.0

OLLAMA_OPTIONS = {
    "temperature",
    "num_predict",
    "top_k",
    "top_p",
    "repeat_penalty",
    "seed",
    "num_ctx",
    "num_batch",
    "num_gpu",
    "main_gpu",
    "low_vram",
    "f16_kv",
    "vocab_only",
    "use_mmap",
    "use_mlock",
    "num_thread",
}

def check_request(body: dict) -> list[str]:
    problems = []

    # Проверка 1: "system" - список сообщений пуст или первое сообщение не с ролью "system"
    messages = body.get("messages", [])
    if not messages or messages[0].get("role") != "system":
        problems.append("system")

    # Проверка 2: "stream" - значение "stream" не равно False
    # Отсутствие ключа - тоже проблема
    if body.get("stream") != False:
        problems.append("stream")

    # Получаем options
    options = body.get("options", {})

    # Проверка 3: "temperature" - в options нет "temperature" или она больше MAX_TEMPERATURE
    if "temperature" not in options or options.get("temperature") > MAX_TEMPERATURE:
        problems.append("temperature")

    # Проверка 4: "num_predict" - в options нет "num_predict"
    if "num_predict" not in options:
        problems.append("num_predict")

    # Проверка 5: "unknown:<имя>" - для каждого ключа options, которого нет в OLLAMA_OPTIONS
    # В порядке ключей (словари в Python 3.7+ сохраняют порядок вставки)
    for key in options:
        if key not in OLLAMA_OPTIONS:
            problems.append(f"unknown:{key}")

    return problems
