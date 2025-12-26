import os
import faiss
import pandas as pd

from typing import List
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore


class RagSystem:
    def __init__(
        self,
        llm_api: str,
        llm_name: str,
        embed_model_name: str,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
        system_prompt: str,
        paths_to_data: List
    ) -> None:
        
        self.__llm_api: str = llm_api
        self.__llm_name: str = llm_name
        self.__embed_model_name: str = embed_model_name
        self.__chunk_size: int = chunk_size
        self.__chunk_overlap: int = chunk_overlap
        self.__top_k: int = top_k
        self.__system_prompt = system_prompt
        self.__index_path = "vector_db_index"

        self.__embedder = HuggingFaceEmbeddings(model_name=self.__embed_model_name)
        self.__text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.__chunk_size,
            chunk_overlap=self.__chunk_overlap
        )

        self.__initialize_vector_store(paths_to_data)

        self.__llm = ChatGoogleGenerativeAI(model=self.__llm_name, google_api_key=self.__llm_api)

        self.__tools = [
            tool(self.__retrieve_context),
            {
                "name": "retrieve_context",
                "description": "Поиск информации в базе данных для ответа на вопросы пользователя."
            }
        ]

        self.__agent = create_agent(self.__llm, self.__tools, system_prompt=self.__system_prompt)

    async def process_query(self, query: str) -> str:
        answer = await self.__agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": query
            }]
        })

        answer = dict(answer["messages"][-1])
        return answer["content"][0]["text"]
    
    def __initialize_vector_store(self, paths_to_data: List):
        if os.path.exists(self.__index_path):
            self.__vector_store = FAISS.load_local(
                self.__index_path, 
                self.__embedder, 
                allow_dangerous_deserialization=True
            )

            return
        
        index = faiss.IndexFlatL2(len(self.__embedder.embed_query("hello world")))
        
        self.__vector_store = FAISS(
            embedding_function=self.__embedder,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        self.__add_data(paths_to_data)

    def __retrieve_context(self, query: str):
        """Retrieve information to help answer a query."""
        retrieved_docs = self.__vector_store.similarity_search(query, k=self.__top_k)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs
    
    def __add_data(self, paths_to_data: List) -> None:
        for path in paths_to_data:
            file_extension = os.path.splitext(path)[1]
            data = None
            
            if file_extension == ".csv":
                data = pd.read_csv(path)
            elif file_extension == ".xlxs":
                data = pd.read_excel(path)

            data = self.__process_table_data(data)
            loader = DataFrameLoader(data, page_content_column="context")
            documents = loader.load()

            all_splits = self.__text_splitter.split_documents(documents)
            self.__vector_store.add_documents(documents=all_splits)

        self.__vector_store.save_local(self.__index_path)

    def __process_table_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data["context"] = data.apply(
            lambda row: "; ".join([f"{col}: {val}" for col, val in row.items()]), 
            axis=1
        )

        return data
