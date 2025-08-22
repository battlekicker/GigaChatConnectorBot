from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class GigaChatService:
    def __init__(self):
        self.credentials = settings.GIGACHAT_CREDENTIALS
        self.verify_ssl = settings.GIGACHAT_VERIFY_SSL
        logger.info("GigaChat service initialized")

    def _convert_to_gigachat_messages(self, messages: list) -> list:
        gigachat_messages = []
        logger.debug(f"Converting {len(messages)} messages to GigaChat format")

        for msg in messages:
            try:
                gigachat_messages.append(
                    Messages(role=MessagesRole(msg["role"]), content=msg["content"])
                )
            except Exception as e:
                logger.warning(f"Error converting message: {e}")

        logger.info(f"Successfully converted {len(gigachat_messages)} messages")
        return gigachat_messages

    def get_response(self, messages: list) -> str:
        try:
            logger.info(f"Requesting response from GigaChat for {len(messages)} messages")

            # Конвертируем сообщения в правильный формат
            gigachat_messages = self._convert_to_gigachat_messages(messages)

            logger.info(f"Sending {len(gigachat_messages)} messages to GigaChat")

            with GigaChat(
                    credentials=self.credentials,
                    verify_ssl_certs=self.verify_ssl
            ) as giga:
                chat = Chat(messages=gigachat_messages)

                logger.debug("Sending request to GigaChat API")

                response = giga.chat(chat)

                logger.info("Successfully received response from GigaChat")
                logger.debug(f"Response: {response.choices[0].message.content[:100]}...")
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"GigaChat error: {str(e)}")
            raise Exception(f"GigaChat service error: {str(e)}")


gigachat_service = GigaChatService()