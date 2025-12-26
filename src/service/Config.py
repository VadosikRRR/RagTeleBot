from typing import List


class Config:
    def __init__(
        self,
        bot_token: str,
        llm_api: str,
        llm_name: str,
        embed_model_name: str,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
        system_prompt: str,
        paths_to_data: List
    ) -> None:
        
        self.__bot_token: str = bot_token
        self.__llm_api: str = llm_api
        self.__llm_name: str = llm_name
        self.__embed_model_name: str = embed_model_name
        self.__chunk_size: int = chunk_size
        self.__chunk_overlap: int = chunk_overlap
        self.__top_k: int = top_k
        self.__system_prompt: str = system_prompt
        self.__paths_to_data: List = paths_to_data

    def get_bot_token(self) -> str:
        return self.__bot_token

    def get_llm_api(self) -> str:
        return self.__llm_api

    def get_llm_name(self) -> str:
        return self.__llm_name

    def get_embed_model_name(self) -> str:
        return self.__embed_model_name

    def get_chunk_size(self) -> int:
        return self.__chunk_size

    def get_top_k(self) -> int:
        return self.__top_k
    
    def get_chunk_overlap(self) -> int:
        return self.__chunk_overlap

    def get_system_prompt(self) -> str:
        return self.__system_prompt

    def get_paths_to_data(self) -> List:
        return self.__paths_to_data[::]
