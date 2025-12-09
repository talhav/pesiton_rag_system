import instructor
from dotenv import load_dotenv
import os
from pydantic import BaseModel


class BedrockLLMService:
    def __init__(
        self,
        model_id: str = "qwen.qwen3-235b-a22b-2507-v1:0",
        region_name: str = "us-east-2",
    ):
        load_dotenv(override=True)
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = os.getenv("BEDROCK_KEY")
        os.environ["AWS_DEFAULT_REGION"] = region_name

        # We have to use the sync client because boto3 Bedrock client is not async !!!
        self.model_id = model_id
        self.llm_client = instructor.from_provider(
            f"bedrock/{self.model_id}", async_client=False
        )

    def generate_text(self, input_text: str, response_model: BaseModel):
        response = self.llm_client.create(
            modelId=self.model_id,
            messages=[{"role": "user", "content": input_text}],
            response_model=response_model,
        )

        return response
