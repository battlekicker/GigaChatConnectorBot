from gigachat import GigaChat
from app.core.config import settings


class GigaChatService:
    def __init__(self):
        self.credentials = settings.GIGACHAT_CREDENTIALS
        self.verify_ssl = settings.GIGACHAT_VERIFY_SSL

    def get_response(self, messages: list) -> str:
        with GigaChat(
                credentials=self.credentials,
                verify_ssl_certs=self.verify_ssl
        ) as giga:
            response = giga.chat(messages)
            return response.choices[0].message.content


giga_chat_service = GigaChatService()