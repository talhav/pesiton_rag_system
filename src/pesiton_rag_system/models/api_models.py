from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Model for a chat message in history"""

    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")


class QueryType(str, Enum):
    """Enum for query types"""

    PRODUCT = "product"
    FACTORY = "factory"


class QueryRequest(BaseModel):
    """Request model for RAG query endpoint"""

    query: str = Field(..., description="The user's question or query", min_length=1)
    type: QueryType = Field(
        default=QueryType.PRODUCT, description="Type of search: product or factory"
    )
    top_k: Optional[int] = Field(
        default=5, description="Number of relevant chunks to retrieve", ge=1, le=20
    )
    chat_history: Optional[List[ChatMessage]] = Field(
        default=None, description="Previous chat messages for context"
    )


class SourceChunk(BaseModel):
    """Model for a source chunk in the response"""

    content: str = Field(..., description="The content of the chunk")
    metadata: dict = Field(default_factory=dict, description="Metadata about the chunk")
    score: Optional[float] = Field(None, description="Relevance score")


class QueryResponse(BaseModel):
    """Response model for RAG query endpoint"""

    query: str = Field(..., description="The original query")
    type: QueryType = Field(..., description="Type of search performed")
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceChunk] = Field(
        default_factory=list, description="Source chunks used to generate the answer"
    )
