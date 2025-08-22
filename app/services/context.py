from app.core.config import settings
from app.utils.logging import get_logger

logger = get_logger("services.context")


class ContextService:
    def __init__(self):
        self.conversations = {}
        logger.info("Context service initialized")

    def get_context(self, user_id: str) -> list:
        if user_id not in self.conversations:
            logger.info(f"Creating new context for user: {user_id}")
            self._initialize_context(user_id)
        else:
            logger.debug(f"Retrieved context for user: {user_id}, messages: {len(self.conversations[user_id])}")

        return self.conversations[user_id]

    def add_message(self, user_id: str, role: str, content: str):
        context = self.get_context(user_id)
        context.append({"role": role, "content": content})

        logger.debug(f"Added message to user {user_id}: {role} - {content[:50]}...")
        logger.info(f"User {user_id} now has {len(context)} messages in context")

        self._trim_context(user_id)

    def clear_context(self, user_id: str):
        if user_id in self.conversations:
            del self.conversations[user_id]
            logger.info(f"Cleared context for user: {user_id}")
        else:
            logger.warning(f"Attempted to clear non-existent context for user: {user_id}")

    def _initialize_context(self, user_id: str):
        self.conversations[user_id] = [{
            "role": "system",
            "content": "Ты - AI-ассистент ГИГА. Всегда представляйся одинаково."
        }]
        logger.debug(f"Initialized context for user: {user_id}")

    def _trim_context(self, user_id: str):
        context = self.conversations[user_id]
        if len(context) > settings.MAX_CONTEXT_MESSAGES:
            old_count = len(context)

            system_msg = context[0]
            recent_msgs = context[-(settings.MAX_CONTEXT_MESSAGES - 1):]
            self.conversations[user_id] = [system_msg] + recent_msgs

            logger.info(
                f"Trimmed context for user {user_id}: {old_count} -> {len(self.conversations[user_id])} messages")


context_service = ContextService()