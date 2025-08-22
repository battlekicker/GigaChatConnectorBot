from decouple import config


class Settings:

    GIGACHAT_CREDENTIALS = config("AUTHORIZATION_KEY")
    GIGACHAT_VERIFY_SSL = config("GIGACHAT_VERIFY_SSL", default=False, cast=bool)

    CORS_ORIGINS = ["*"]

    MAX_CONTEXT_MESSAGES = config("MAX_CONTEXT_MESSAGES", default=20, cast=int)

    LOG_LEVEL = config("LOG_LEVEL", default="INFO")

settings = Settings()