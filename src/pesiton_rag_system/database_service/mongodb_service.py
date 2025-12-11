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
                    "numCandidates": number_of_candiates,
                    "limit": top_k,
                }
            },
            {"$addFields": {"score": {"$meta": "vectorSearchScore"}}},
            {
                "$lookup": {
                    "from": "factories",  # Name of your factory collection
                    "localField": "factoryId",  # Field in product collection
                    "foreignField": "_id",  # Field in factory collection
                    "as": "factory",  # Name for the joined data
                }
            },
            {
                "$unwind": {
                    "path": "$factory",
                    "preserveNullAndEmptyArrays": True,  # Keep products even if factory not found
                }
            },
            {
                "$project": {
                    "embedding": 0  # Exclude the embedding field
                }
            },
        ]

        results = await collection.aggregate(pipeline).to_list(length=top_k)
        return results

    def close_client(self):
        self.client.close()
