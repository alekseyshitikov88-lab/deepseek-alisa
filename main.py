import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    response = requests.post(
        DEEPSEEK_API_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": user_text}],
        }
    )
   response = requests.post(
    DEEPSEEK_API_URL,
    headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
    json={
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": user_text}],
    }
)

# Проверяем, что запрос к Groq прошел успешно
if response.status_code != 200:
    # Выводим в логи Render текст ошибки от Groq
    print("Ошибка от Groq:", response.status_code, response.text)
    # Возвращаем заглушку, чтобы сервер не падал с ошибкой 500
    answer = "Извините, произошла ошибка при обработке запроса."
else:
    # Если все хорошо, извлекаем ответ
    answer = response.json()["choices"][0]["message"]["content"]

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
