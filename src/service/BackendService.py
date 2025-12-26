import logging

from typing import Optional

from src.service.Config import Config
from src.bot.TelegramBot import TelegramBot


LOGGER = logging.getLogger(__name__)

class BackendService:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.__rag_system = None
        self.__bot: Optional[TelegramBot] = None

        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        LOGGER.info("Service is ready")

    async def run(self):
        self.__bot = TelegramBot(token=self.__config.get_bot_token(), backend=self)
        LOGGER.info("Bot is running")
        await self.__bot.run()

    async def process_user_query(self, user_id: str, query: str):
        return "Bro, sorry, now I can't."
