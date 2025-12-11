from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryType(str, Enum):
    """Enum for query types"""

    PRODUCT = "product"
    FACTORY = "factory"


class ChatMessage(BaseModel):
    role: str
    content: str


class Location(BaseModel):
    country: str
    label: str


class Rating(BaseModel):
    value: float
    scale: int
    source: str


class FloorSpace(BaseModel):
    value: float
    unit: str


class Certification(BaseModel):
    name: str


class FactoryInfo(BaseModel):
    """Factory information embedded in product search results"""

    id: str = Field(alias="_id")
    userId: Optional[str] = None
    companyName: str
    location: Optional[Location] = None
    establishedYear: Optional[int] = None
    businessType: Optional[str] = None
    staffBreakdown: Optional[Dict[str, Any]] = None
    mainMarkets: Optional[List[str]] = None
    badges: Optional[List[str]] = None
    rating: Optional[Rating] = None
    ccfpGrade: Optional[str] = None
    aqlStandard: Optional[str] = None
    ccfpScoresBreakdown: Optional[Dict[str, Any]] = None
    floorSpaceTotal: Optional[FloorSpace] = None
    floorSpaceDetails: Optional[Dict[str, Any]] = None
    staffBreakdownDetails: Optional[Dict[str, Any]] = None
    productionLines: Optional[int] = None
    equipmentCounts: Optional[Dict[str, Any]] = None
    factoryCertifications: Optional[List[Certification]] = None
    productCertifications: Optional[List[Any]] = None
    qualityAuditReports: Optional[List[Any]] = None
    status: Optional[str] = None
    isPreferredSupplier: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        populate_by_name = True


class MOQ(BaseModel):
    quantity: Optional[int] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class PricingTier(BaseModel):
    minQuantity: Optional[int] = None
    maxQuantity: Optional[int] = None
    unitPrice: Optional[float] = None
    currency: Optional[str] = None


class SourceChunk(BaseModel):
    """Enhanced source chunk with full product and factory data"""

    # Product fields
    id: str = Field(alias="_id")
    factoryId: Optional[str] = None
    productName: str
    modelNumber: Optional[str] = None
    description: str
    badges: Optional[List[str]] = None
    imageUrls: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    moq: Optional[MOQ] = None
    pricingTiers: Optional[List[PricingTier]] = None
    tradeTerms: Optional[List[str]] = None
    detailedSpecs: Optional[Dict[str, Any]] = None
    certifications: Optional[List[str]] = None
    usageScenarios: Optional[List[str]] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    isPublishedToMarketplace: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    productLink: Optional[str] = None
    score: Optional[float] = None

    # Factory data
    factory: Optional[FactoryInfo] = None

    class Config:
        populate_by_name = True


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    type: QueryType = Field(
        default=QueryType.PRODUCT, description="Type of search: product or factory"
    )
    top_k: int = Field(default=5, description="Number of results to retrieve")
    chat_history: Optional[List[ChatMessage]] = Field(
        default=None, description="Previous conversation messages"
    )


class QueryResponse(BaseModel):
    query: str
    type: QueryType = Field(..., description="Type of search performed")
    answer: str
    sources: List[SourceChunk]
