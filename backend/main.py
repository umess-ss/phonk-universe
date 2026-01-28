from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import track_collection, client, Track
from fastapi.encoders import jsonable_encoder


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping_server():
    try:
        await client.admin.command("ping")
        return {"status": "Success", "message": "Connected to MongoDB Atlas!!!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/add-track")
async def create_track(track: Track):
    # 1. convert the pydantic model to dictonary
    track_dict = jsonable_encoder(track)

    # 2. Insert into MongoDB
    new_track = await track_collection.insert_one(track_dict)

    # 3. Find the created track to return it
    created_track = await track_collection.find_one({"id": new_track.inserted_id})

    # 4. Convert MongoDB _id to string for JSON compactibility
    if created_track:
        created_track["_id"] = str(created_track["_id"])
        return {"status": "success", "data": create_track}

    raise HTTPException(status_code=404, detail="Track could not be created")


@app.get("/tracks")
async def get_tracks():
    tracks=[]
    async for track in track_collection.find():
        track["_id"] = str(track["_id"])    # convert mongodbid to string
        tracks.append(track)
    return tracks








if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
