import logging
from app.core.config import settings


def setup_logging():
    """Только консольное логирование"""

    # Простая настройка
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    print(f"Logging initialized with level: {settings.LOG_LEVEL}")


def get_logger(name: str) -> logging.Logger:
    """Получение логгера с указанным именем"""
    return logging.getLogger(f"app.{name}")