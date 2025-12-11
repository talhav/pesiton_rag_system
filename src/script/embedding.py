import asyncio
import json
import boto3
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = os.getenv("BEDROCK_KEY")

# MongoDB connection
MONGO_URI = os.getenv("MONGODB_URL")
REGION = "us-east-1"
MODEL_ID = "cohere.embed-v4:0"

bedrock = boto3.client(service_name="bedrock-runtime", region_name=REGION)


def create_embedding_text(product):
    """Concatenate product fields into a single string"""
    fields = {
        "description": product.get("description", ""),
        "badges": ", ".join(product.get("badges", [])),
        "colors": ", ".join(product.get("colors", [])),
        "moq": str(product.get("moq", "")),
        "pricingTiers": str(product.get("pricingTiers", "")),
        "tradeTerms": ", ".join(product.get("tradeTerms", [])),
        "detailedSpecs": str(product.get("detailedSpecs", "")),
        "certifications": ", ".join(product.get("certifications", [])),
        "usageScenarios": ", ".join(product.get("usageScenarios", [])),
    }

    text = ", ".join([f"{key}: {value}" for key, value in fields.items()])
    print(f"Created embedding text ({len(text)} chars)")
    return text


def generate_embedding(text):
    """Generate embedding from text"""
    print("Calling Bedrock API...")
    body = json.dumps(
        {"texts": [text], "input_type": "search_document", "embedding_types": ["float"]}
    )

    response = bedrock.invoke_model(
        body=body, modelId=MODEL_ID, accept="*/*", contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body["embeddings"]["float"][0]
    print(f"Generated embedding (dimension: {len(embedding)})")
    return embedding


async def process_products():
    """Read products, generate embeddings, and update records"""
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.pesiton
    collection = db.products

    # Get first 10 products without embeddings
    print("Fetching products without embeddings...")
    # products = (
    #     await collection.find({"embedding": {"$exists": False}})
    #     .sort("createdAt", 1)
    #     .limit(10)
    #     .to_list(length=10)
    # )
    products = (
        await collection.find({"embedding": {"$exists": False}})
        .sort("createdAt", 1)
        .to_list(length=None)
    )
    print(f"Found {len(products)} products to process\n")

    updated_ids = []

    for i, product in enumerate(products, 1):
        print(f"Processing product {i}/{len(products)}: {product['_id']}")
        embedding_text = create_embedding_text(product)
        embedding = generate_embedding(embedding_text)
        await update_embedding(collection, product["_id"], embedding)
        updated_ids.append(product["_id"])
        print(f"Updated product {product['_id']}\n")

    client.close()

    print(f"Completed! Updated {len(updated_ids)} records:")
    for product_id in updated_ids:
        print(f"  - {product_id}")


async def update_embedding(collection, product_id, embedding):
    """Update product record with embedding"""
    print("Writing to MongoDB...")
    await collection.update_one({"_id": product_id}, {"$set": {"embedding": embedding}})


if __name__ == "__main__":
    asyncio.run(process_products())