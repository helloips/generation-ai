import ollama

response = ollama.generate(
    model="qwen3.5:4b",
    prompt="Какой HTTP-код означает успешное создание ресурса? Ответь только числом.",
    think=False,
    options={"temperature": 0, "num_predict": 20}
)
print(response.response)
