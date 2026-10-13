# task-template

Шаблон FastAPI-сервиса для быстрого деплоя на Render.

Локальный запуск:

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload

Render: Web Service, Docker (Dockerfile в корне), переменная PORT подставляется сама.
