from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import track_collection, client, Track
from fastapi.encoders import jsonable_encoder
from typing import Optional
from bson import ObjectId

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


    async for track in cursor:
        track["_id"] = str(track["_id"])    # convert mongodbid to string
        tracks.append(track)
    return {"status":"success", "count": len(tracks), "data": tracks}


@app.get("/tracks/{track_id}")
async def get_track(track_id: str):
    """Get a specific track by id"""
    try:
        track = await track_collection.find_one({"_id": ObjectId(track_id)})
        if track:
            track["_id"] = str(track["_id"])
            return {"status": "success", "data": track}
        raise HTTPException(status_code=404, detail="Track not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Track ID")




@app.delete("/tracks/{track_id}")
async def delete_track(track_id: str):
    """Delete Track by id"""
    try:
        result = await track_collection.delete_one({"_id": ObjectId(track_id)})
        if result.deleted_count > 0:
            return {"status": "success", "message": "Track deleted successfully..."}
            
        raise HTTPException(status_code=404, detail="Track not found")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    

@app.get("/genres")
async def get_genres():
    """Get unique genre"""
    genres = await track_collection.distinct("genre")
    return {"status": "success", "data": genres}


@app.get("/artists")
async def get_artists():
    """Get unique artists"""
    artists = await track_collection.distinct("artist")
    return {"status": "success", "data": artists}


@app.get("/tracks/search/{query}")
async def search_tracks(query: str):
    """Search tracks by title or artist"""
    # Simple regex search (case-insensitive)
    search_query = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"artist": {"$regex": query, "$options": "i"}}
        ]
    }
    tracks = []
    cursor = track_collection.find(search_query).limit(20)
    async for track in cursor:
        track["_id"] = str(track["_id"])
        tracks.append(track)
    return {"status": "success", "data": tracks}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
