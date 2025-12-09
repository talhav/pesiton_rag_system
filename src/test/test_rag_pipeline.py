import asyncio
import os

from dotenv import load_dotenv

from pesiton_rag_system.rag_pipeline.pipeline import RAGPipeline

load_dotenv(override=True)


async def test_rag_pipeline_initialization(user_query: str):
    try:
        pipeline: RAGPipeline = RAGPipeline(
            mongo_url=os.getenv("MONGODB_URL"),
            mongo_db_name="pesiton",
            embedding_model_region="us-east-1",
            embedding_model_id="cohere.embed-v4:0",
            llm_model_id="qwen.qwen3-235b-a22b-2507-v1:0",
            llm_model_region="us-east-2",
        )

        # test retrieval
        user_query = user_query
        collection_name = os.getenv("COLLECTION_NAME")
        top_k = 3
        retrieved_docs = await pipeline.retrieve(
            user_query=user_query, collection_name=collection_name, top_k=top_k
        )
        print("Retrieved documents:")
        print(retrieved_docs)

        # test response generation
        llm_response = await pipeline.generate_response(
            user_query=user_query,
            context="\n".join([doc["description"] for doc in retrieved_docs]),
        )

        print("\nFirst response:")
        print(llm_response)

        # Test with chat history - follow-up question
        follow_up_query = "What about wireless options?"

        # Format chat history
        chat_history = f"user: {user_query}\nassistant: {llm_response.answer}"

        # Retrieve docs for follow-up
        follow_up_docs = await pipeline.retrieve(
            user_query=follow_up_query, collection_name=collection_name, top_k=top_k
        )

        # Generate response with chat history
        follow_up_response = await pipeline.generate_response(
            user_query=follow_up_query,
            context="\n".join([doc["description"] for doc in follow_up_docs]),
            chat_history=chat_history,
        )

        print("\nFollow-up response with chat history:")
        print(follow_up_response)

    # close the mongodb client after test
    except Exception as e:
        print(f"Error during RAG pipeline test: {e}")
    finally:
        pipeline.mongodb_service.close_client()


if __name__ == "__main__":
    test_query = "headphones with active noise cancellation for under $100"
    asyncio.run(test_rag_pipeline_initialization(user_query=test_query))
