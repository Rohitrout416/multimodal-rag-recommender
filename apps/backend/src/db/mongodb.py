from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URL)
        print("Connected to MongoDB")

    async def disconnect(self):
        if self.client:
            self.client.close()
        print("Disconnected from MongoDB")


    def get_db(self):
        return self.client[settings.MONGO_DB_NAME]

db = Database()

async def get_database():
    return db.get_db()
