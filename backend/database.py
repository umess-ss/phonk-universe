from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_URL")


client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.PhonkUniverseDB
track_collection = database.get_collection("tracks")


class Track(BaseModel):
    title: str = Field(...)
    artist: str = Field(...)
    platform: str = Field(default="youtub or spotify")
    externalID: str = Field(...)


    class Config:
        # This allows you to see examples in your FastAPI /docs
        json_schema_extra = {
            "example": {
                "title": "Sahara",
                "artist": "Hensonn",
                "platform": "youtube",
                "externalID": "hH9MtcFpP5M"
            }
        }