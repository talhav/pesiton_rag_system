import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pesiton_rag_system.models.api_models import (
    QueryRequest,
    QueryResponse,
    SourceChunk,
)
from pesiton_rag_system.rag_pipeline.pipeline import RAGPipeline

load_dotenv(override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rag_pipeline = RAGPipeline(
        mongo_url=os.getenv("MONGODB_URL"),
        mongo_db_name=os.getenv("MONGO_DB_NAME", "pesiton"),
        embedding_model_region=os.getenv("EMBEDDING_MODEL_REGION", "us-east-1"),
        embedding_model_id=os.getenv("EMBEDDING_MODEL_ID", "cohere.embed-v4:0"),
        llm_model_id=os.getenv("LLM_MODEL_ID", "qwen.qwen3-235b-a22b-2507-v1:0"),
        llm_model_region=os.getenv("LLM_MODEL_REGION", "us-east-2"),
    )

    # Store in app state
    app.state.rag_pipeline = rag_pipeline

    yield

    rag_pipeline.mongodb_service.close_client()


app = FastAPI(
    title="CueGrowth ML Realtime Message API",
    version="1.0.0",
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query the RAG system with a question and get an answer with sources.
    """
    if not hasattr(app.state, "rag_pipeline") or app.state.rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")

    try:
        # Determine collection based on type
        if request.type == "product":
            collection_name = os.getenv("COLLECTION_NAME")
        elif request.type == "factory":
            collection_name = os.getenv("FACTORY_COLLECTION_NAME")
        else:
            raise HTTPException(status_code=400, detail="Invalid query type")

        if not collection_name:
            raise HTTPException(
                status_code=500,
                detail=f"Collection name for type '{request.type}' not configured",
            )

        # Retrieve relevant documents
        retrieved_docs = await app.state.rag_pipeline.retrieve(
            user_query=request.query,
            collection_name=collection_name,
            top_k=request.top_k,
        )

        # Generate context from retrieved documents
        context = "\n".join([doc.get("description", "") for doc in retrieved_docs])

        # Format chat history if provided
        chat_history_str = None
        if request.chat_history:
            chat_history_str = "\n".join(
                [f"{msg.role}: {msg.content}" for msg in request.chat_history]
            )

        # Generate response using LLM with chat history
        llm_response = await app.state.rag_pipeline.generate_response(
            user_query=request.query, context=context, chat_history=chat_history_str
        )

        # Extract answer string from LLMResponseModel
        answer = (
            llm_response.answer
            if hasattr(llm_response, "answer")
            else str(llm_response)
        )

        # Convert retrieved docs to SourceChunk models
        sources = []
        for doc in retrieved_docs:
            # Convert ObjectId to string for _id fields
            doc_copy = doc.copy()
            if "_id" in doc_copy:
                doc_copy["_id"] = str(doc_copy["_id"])
            if "factoryId" in doc_copy and doc_copy["factoryId"]:
                doc_copy["factoryId"] = str(doc_copy["factoryId"])
            if "userId" in doc_copy and doc_copy["userId"]:
                doc_copy["userId"] = str(doc_copy["userId"])

            # Handle factory data if present
            if "factory" in doc_copy and doc_copy["factory"]:
                factory = doc_copy["factory"]
                if "_id" in factory:
                    factory["_id"] = str(factory["_id"])
                if "userId" in factory and factory["userId"]:
                    factory["userId"] = str(factory["userId"])

            sources.append(SourceChunk(**doc_copy))

        # Build response with type
        response = QueryResponse(
            query=request.query,
            type=request.type,
            answer=answer,
            sources=sources,
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
