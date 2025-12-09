import asyncio

from pesiton_rag_system.database_service.mongodb_service import MongoDBService
from pesiton_rag_system.embedding_service.bedrock_embeddings import BedrockEmbeddings
from pesiton_rag_system.llm_service.bedrock_llm_service import BedrockLLMService
from pesiton_rag_system.models.llm_response_model import LLMResponseModel
from pesiton_rag_system.prompt_service import PromptManager


class RAGPipeline:
    def __init__(
        self,
        mongo_url: str,
        mongo_db_name: str,
        embedding_model_region: str,
        embedding_model_id: str,
        llm_model_id: str,
        llm_model_region: str,
    ):
        self.mongodb_service: MongoDBService = MongoDBService(
            uri=mongo_url, db_name=mongo_db_name
        )
        self.embedding_service = BedrockEmbeddings(
            region_name=embedding_model_region, model_id=embedding_model_id
        )
        self.llm_service = BedrockLLMService(
            model_id=llm_model_id, region_name=llm_model_region
        )
        self.prompt_manager = PromptManager()

    async def retrieve(self, user_query: str, collection_name: str, top_k: int):
        print("Generating embedding for user query")
        # Step 1: Get embedding for user query
        # calling using asyncio.to_thread to run the synchronous method in a separate thread
        query_embedding = await asyncio.to_thread(
            self.embedding_service.get_embedding, text=user_query
        )

        # Step 2: Perform vector search in MongoDB
        print("Performing vector search in MongoDB")
        retrieved_docs = await self.mongodb_service.vector_search(
            collection_name=collection_name,
            query_vector=query_embedding,
            top_k=top_k,
        )

        return retrieved_docs

    async def generate_response(
        self, user_query: str, context: str, chat_history: str = None
    ):
        print("Generating response using LLM with context")

        # Build the prompt with chat history if provided
        prompt_parts = []

        if chat_history:
            prompt_parts.append("Previous conversation:")
            prompt_parts.append(chat_history)
            prompt_parts.append("\n---\n")

        prompt_parts.append(f"Context: {context}")
        prompt_parts.append(f"\nQuestion: {user_query}")

        full_prompt = "\n".join(prompt_parts)

        response = self.llm_service.generate_text(
            input_text=full_prompt, response_model=LLMResponseModel
        )

        return response
