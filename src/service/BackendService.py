import logging

from typing import Optional

from src.service.Config import Config
from src.rag.RagSystem import RagSystem
from src.bot.TelegramBot import TelegramBot


LOGGER = logging.getLogger(__name__)

class BackendService:
    def __init__(self, config: Config) -> None:
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        LOGGER.info("Service is preparing...")
        
        self.__config: Config = config
        self.__bot: Optional[TelegramBot] = None
        self.__rag_system: RagSystem = RagSystem(
            llm_api=config.get_llm_api(),
            llm_name=config.get_llm_name(),
            embed_model_name=config.get_embed_model_name(),
            chunk_size=config.get_chunk_size(),
            chunk_overlap=config.get_chunk_overlap(),
            top_k=config.get_top_k(),
            system_prompt=config.get_system_prompt(),
            paths_to_data=config.get_paths_to_data()
        )

        LOGGER.info("Rag system is ready")
        LOGGER.info("Service is ready")

    async def run(self):
        self.__bot = TelegramBot(token=self.__config.get_bot_token(), backend=self)
        LOGGER.info("Bot is running")
        await self.__bot.run()

    async def process_user_query(self, query: str):
        result = await self.__rag_system.process_query(query)
        return result
