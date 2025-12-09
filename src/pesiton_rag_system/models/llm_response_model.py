from pydantic import BaseModel


class LLMResponseModel(BaseModel):
    answer: str
