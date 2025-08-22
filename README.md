# GigaChatConnectorBot

Проект представляет собой чат-бота с искусственным интеллектом на основе GigaChat API, построенного по микросервисной архитектуре с использованием FastAPI и aiogram.

Данные бот обладает возможностью интеллектуального диалога с Gigachat с поддержкой контекста в режиме стриминга. Контекст разговора сохраняется.

### Пошаговое руководство по использованию:

1. Клонировать репозиторий командой

    `git clone https://github.com/battlekicker/GigaChatConnectorBot`


2. Создать виртуальное окружение внутри проекта

    `python -m venv .venv`


3. Активировать виртуальное окружение

    для Windows:
     `.\.venv\Scripts\activate` 
    
    для Linux/Mac:
    `source .venv/bin/activate`


4. Произвести установку зависимостей

    `pip install -r requirements.txt`


5. В корне проекта создать файл .env следующего содержания

    `BOT_TOKEN=your_telegram_bot_token`
    
    `AUTHORIZATION_KEY=your_gigachat_authorization_key`
    
    `LOG_LEVEL=INFO`
    
    `GIGACHAT_VERIFY_SSL=False`
    
    `MAX_CONTEXT_MESSAGES=20`


6. Запуск сервиса командой в корне проекта

    `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

    Сервис будет доступен по адресу http://localhost:8000


7. Для запуска Telegram бота внутри пакета app (`cd app`) использовать

    `python bot.py`


### API Endpoints

   1. GET /api/v1/status (Проверка статуса сервиса)
   
   `curl http://localhost:8000/api/v1/status`


   2. POST /api/v1/chat (Отправка сообщения)


      Для Linux/Mac:
   
      `curl -X POST http://localhost:8000/api/v1/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Привет!", "user_id": "user123"}'`
      
      Для Windows:
   
      ``curl.exe -X POST "http://localhost:8000/api/v1/chat" `
        -H "Content-Type: application/json" `
        -d "{\"message\": \"Привет!\", \"user_id\": \"user123\"}"``

