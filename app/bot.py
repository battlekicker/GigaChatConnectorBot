from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiohttp
import asyncio
import json
import logging
from decouple import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("bot")

router = Router()
API_BASE_URL = "http://localhost:8000/api/v1"


async def handle_streaming_response(message: Message, user_input: str):
    try:
        payload = {
            "message": user_input,
            "user_id": str(message.from_user.id)
        }

        logger.info(f"Starting SSE streaming for user {message.from_user.id}")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{API_BASE_URL}/chat",
                    json=payload,
                    timeout=30,
                    headers={'Accept': 'text/event-stream'}
            ) as response:

                logger.info(f"Response status: {response.status}")
                logger.info(f"Content-Type: {response.headers.get('Content-Type')}")

                if response.status == 200:
                    buffer = ""
                    sent_message = None

                    async for line in response.content:
                        try:
                            line_str = line.decode('utf-8').strip()
                            logger.debug(f"SSE line: {line_str}")

                            if line_str.startswith('data: '):
                                json_str = line_str[6:]
                                if json_str:
                                    try:
                                        data = json.loads(json_str)
                                        logger.debug(f"Parsed SSE data: {data}")

                                        if 'chunk' in data:
                                            buffer += data['chunk']
                                            logger.debug(f"Buffer: {buffer}")

                                            if sent_message is None:
                                                sent_message = await message.answer(buffer)
                                            else:
                                                try:
                                                    await sent_message.edit_text(buffer)
                                                except Exception as e:
                                                    logger.warning(f"Could not edit message: {e}")
                                                    sent_message = await message.answer(buffer)

                                            await asyncio.sleep(0.1)

                                        if data.get('complete', False):
                                            logger.info("SSE stream completed successfully")
                                            break

                                        if 'error' in data:
                                            error_msg = data['error']
                                            logger.error(f"SSE stream error: {error_msg}")
                                            await message.answer(f"Ошибка: {error_msg}")
                                            break

                                    except json.JSONDecodeError as e:
                                        logger.warning(f"JSON decode error in SSE: {e}")
                                        continue

                        except UnicodeDecodeError as e:
                            logger.warning(f"Unicode decode error: {e}")
                            continue
                        except Exception as e:
                            logger.warning(f"Error processing SSE line: {e}")
                            continue

                    logger.info(f"Final message: {buffer}")
                    return True

                else:
                    error_text = await response.text()
                    logger.error(f"API error {response.status}: {error_text}")
                    await message.answer(f"Ошибка сервера: {response.status}")
                    return False

    except asyncio.TimeoutError:
        logger.error("Timeout during SSE streaming")
        await message.answer("Таймаут при обработке запроса")
        return False

    except aiohttp.ClientError as e:
        logger.error(f"HTTP client error during SSE: {e}")
        await message.answer("Ошибка соединения с сервером")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during SSE streaming: {e}")
        await message.answer("Неожиданная ошибка при обработке")
        return False


async def check_api_status() -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/status", timeout=5) as response:
                return response.status == 200
    except:
        return False


@router.message(Command("start"))
async def cmd_start(message: Message):
    api_online = await check_api_status()
    if api_online:
        await message.answer("Привет! Я AI-ассистент ГИГА. Чем могу помочь?")
    else:
        await message.answer("Сервис временно недоступен. Попробуйте позже.")


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f"{API_BASE_URL}/context/{message.from_user.id}",
                    timeout=10
            ) as response:
                if response.status == 200:
                    await message.answer("Контекст разговора очищен!")
                else:
                    await message.answer("Не удалось очистить контекст.")
    except Exception as e:
        logger.error(f"Clear context error: {e}")
        await message.answer("Ошибка при очистке контекста.")


@router.message()
async def handle_all_messages(message: Message):
    if not message.text or message.text.startswith('/'):
        return

    api_online = await check_api_status()
    if not api_online:
        await message.answer("⚠️ Сервис временно недоступен. Попробуйте позже.")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(0.5)

    success = await handle_streaming_response(message, message.text)

    if not success:
        await message.answer("Не удалось обработать запрос. Попробуйте еще раз.")


async def main():
    try:
        bot = Bot(
            token=config('BOT_TOKEN'),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            )
        )

        dp = Dispatcher()
        dp.include_router(router)

        try:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook deleted successfully")
        except Exception as e:
            logger.warning(f"Error deleting webhook: {e}")

        if await check_api_status():
            logger.info("API сервис доступен!")
        else:
            logger.warning("API сервис недоступен!")

        logger.info("Starting bot with SSE support...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())