import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db["users"]

async def create_user(user: dict):
    result = await users_collection.insert_one(user)
    return str(result.inserted_id)

async def get_all_users():
    users = await users_collection.find().to_list(100)
    for u in users:
        u["_id"] = str(u["_id"])  # Convert ObjectId to string
    return users
