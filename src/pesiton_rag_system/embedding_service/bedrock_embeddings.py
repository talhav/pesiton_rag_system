import boto3
from dotenv import load_dotenv
import os
import json


class BedrockEmbeddings:
    def __init__(
        self, region_name: str = "us-east-1", model_id: str = "cohere.embed-v4:0"
    ):
        load_dotenv(override=True)
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = os.getenv("BEDROCK_KEY")

        self.client = boto3.client(
            service_name="bedrock-runtime", region_name=region_name
        )
        self.embedding_model_id = model_id

    # this function is left synchronous because Bedrock's boto3 client does not support async calls
    # so to make it async we would have to run it using asyncio.to_thread when calling it !!!

    def get_embedding(self, text: str):
        try:
            body = json.dumps(
                {
                    "texts": [text],
                    "input_type": "search_query",
                    "embedding_types": ["float"],
                }
            )

            response = self.client.invoke_model(
                body=body,
                modelId=self.embedding_model_id,
                accept="*/*",
                contentType="application/json",
            )

            response_body = json.loads(response.get("body").read())

            return response_body["embeddings"]["float"][0]

        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise e
