from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import track_collection


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tracks")
async def get_tracks():
    tracks=[]
    async for track in track_collection.find():
        track["_id"] = str(track["_id"])    # convert mongodbid to string
        tracks.append(track)
    return tracks










origins = [
    "http://localhost:5173",
]

