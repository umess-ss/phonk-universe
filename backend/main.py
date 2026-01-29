from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import track_collection, client, Track
from fastapi.encoders import jsonable_encoder
from typing import Optional

app = FastAPI(
    title = "Phonk Universe API",
    description="API For Phonk Universe Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message":"Welcome to phonk universe api", "status": "online"}


@app.get("/ping")
async def ping_server():
    try:
        await client.admin.command("ping")
        return {"status": "Success", "message": "Connected to MongoDB Atlas!!!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/add-track")
async def create_track(track: Track):
    """Add a new track to database"""

    existed_track = await track_collection.find_one({
        "externalID": track.externalID,
        "platform": track.platform
    })

    if existed_track:
        raise HTTPException(status_code=400, detail="Track Already Exists")
    # 1. convert the pydantic model to dictonary
    track_dict = jsonable_encoder(track)

    # 2. Insert into MongoDB
    result = await track_collection.insert_one(track_dict)

    # 3. Instead of searching again, just add the new ID to our dictionary
    track_dict["_id"] = str(result.inserted_id)

    return {"status": "success","message":"Track Added Successfully", "data": track_dict}


@app.get("/tracks")
async def get_tracks(
    genre: Optional[str] =None,
    platform: Optional[str]=None,
    limit: int = 50
    ):
    """Get All Tracks with Optional Filtering"""

    query = {}

    if genre:
        query["genre"] = genre
    if platform:
        query["platform"] = platform

    tracks=[]
    cursor = track_collection.find(query).limit(limit)


    async for track in track_collection.find():
        track["_id"] = str(track["_id"])    # convert mongodbid to string
        tracks.append(track)
    return {"status":"success", "count": len(tracks), "data": tracks}








if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
