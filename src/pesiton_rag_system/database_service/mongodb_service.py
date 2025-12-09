from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBService:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def vector_search(
        self,
        collection_name: str,
        query_vector: list,
        top_k: int,
        candiate_multiplier: int = 10,
    ):
        number_of_candiates = top_k * candiate_multiplier
        collection = self.db[collection_name]

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": number_of_candiates,  # ANN used here to check with k*10 candidates and the limit is used to return top_k results. Increase this value if recall is low.
                    "limit": top_k,
                }
            },
            {
                # What fields to return - customize as needed
                "$project": {
                    "_id": 1,
                    "productName": 1,
                    "description": 1,
                    "modelNumber": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]

        results = await collection.aggregate(pipeline).to_list(length=top_k)
        return results

    def close_client(self):
        self.client.close()
