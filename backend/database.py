from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
from typing import Optional


load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_URL")


client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.PhonkUniverseDB
track_collection = database.get_collection("tracks")


class Track(BaseModel):
    title: str = Field(..., description="Track Title")
    artist: str = Field(..., description="Track Artist")
    genre: Optional[str] = Field(default="Phonk", description="Music Genre")
    platform: str = Field(..., description="Platform youtube or sportfy")
    externalID: str = Field(..., description="Platform specific id")
    thumbnail: Optional[str] = Field(default=None, description="Thumbnail URL")


    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sahara",
                "artist": "Hensonn",
                "genre": "Drift Phonk",
                "platform": "youtube",
                "externalID": "hH9MtcFpP5M",
                "thumbnail": "https://img.youtube.com/vi/hH9MtcFpP5M/0.jpg"
            }
        }