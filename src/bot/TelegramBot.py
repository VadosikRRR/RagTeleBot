from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Dict
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

from src.bot.messages import *


if TYPE_CHECKING:
    from src.service.BackendService import BackendService

class TelegramBot:
    def __init__(self, token: str, backend: BackendService) -> None:
        self.__backend: BackendService = backend
        self.__bot: AsyncTeleBot = AsyncTeleBot(token)

        self.__setup_handlers()

    async def run(self):
        await self.__bot.polling(none_stop=True)

    def __setup_handlers(self) -> None:
        @self.__bot.message_handler(commands=["start", "help"])
        async def send_start_message(message: Message):
            await self.__bot.reply_to(message, START_MESSAGE)

        @self.__bot.message_handler()
        async def handle_message(message: Message):
            user_id = message.from_user.id
            await self.__bot.send_chat_action(user_id, 'typing')
            answer = await self.__backend.process_user_query(message.text)
            await self.__bot.reply_to(message, answer)
