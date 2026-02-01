"""
Seed script to populate the database with sample Phonk tracks.
Run this after setting up your MongoDB connection.

Usage: python seed_data.py
"""

import asyncio
from database import track_collection, client

async def seed_tracks():
    print("🎵 Starting database seeding...")
    
    # Check if tracks already exist
    existing_count = await track_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} tracks.")
        response = input("Do you want to add more tracks? (y/n): ")
        if response.lower() != 'y':
            print("Seeding cancelled.")
            return
    
    sample_tracks = [
        {
            "title": "Sahara",
            "artist": "Hensonn",
            "genre": "Drift Phonk",
            "platform": "youtube",
            "externalID": "hH9MtcFpP5M",
            "thumbnail": "https://img.youtube.com/vi/hH9MtcFpP5M/0.jpg"
        },
        {
            "title": "METAMORPHOSIS",
            "artist": "INTERWORLD",
            "genre": "Drift Phonk",
            "platform": "youtube",
            "externalID": "b0bSJ-5IMbE",
            "thumbnail": "https://img.youtube.com/vi/b0bSJ-5IMbE/0.jpg"
        },
        {
            "title": "MURDER IN MY MIND",
            "artist": "Kordhell",
            "genre": "Aggressive Phonk",
            "platform": "youtube",
            "externalID": "ngXP5xYldV4",
            "thumbnail": "https://img.youtube.com/vi/ngXP5xYldV4/0.jpg"
        },
        {
            "title": "SHADOW",
            "artist": "SXID",
            "genre": "Dark Phonk",
            "platform": "youtube",
            "externalID": "rPya6Yxdj0I",
            "thumbnail": "https://img.youtube.com/vi/rPya6Yxdj0I/0.jpg"
        },
        {
            "title": "COWBOYS",
            "artist": "KUTE",
            "genre": "Drift Phonk",
            "platform": "youtube",
            "externalID": "zOWLdP_8rVg",
            "thumbnail": "https://img.youtube.com/vi/zOWLdP_8rVg/0.jpg"
        },
        {
            "title": "MIDNIGHT",
            "artist": "LXST CXNTURY",
            "genre": "House Phonk",
            "platform": "youtube",
            "externalID": "xpxQlIL9CXo",
            "thumbnail": "https://img.youtube.com/vi/xpxQlIL9CXo/0.jpg"
        },
        {
            "title": "FUNK ESTRANHO",
            "artist": "MXDNIGHT",
            "genre": "Brazilian Phonk",
            "platform": "youtube",
            "externalID": "zLTlG7lJuAc",
            "thumbnail": "https://img.youtube.com/vi/zLTlG7lJuAc/0.jpg"
        },
        {
            "title": "SMOKE IT OFF",
            "artist": "LXST CXNTURY",
            "genre": "Chill Phonk",
            "platform": "youtube",
            "externalID": "0PXQvvvQZn4",
            "thumbnail": "https://img.youtube.com/vi/0PXQvvvQZn4/0.jpg"
        },
        {
            "title": "DEVIL EYES",
            "artist": "HIPPIE SABOTAGE",
            "genre": "Dark Phonk",
            "platform": "youtube",
            "externalID": "ss9ygQqqLA4",
            "thumbnail": "https://img.youtube.com/vi/ss9ygQqqLA4/0.jpg"
        },
        {
            "title": "NIGHT DRIVE",
            "artist": "DVRST",
            "genre": "Drift Phonk",
            "platform": "youtube",
            "externalID": "VtpFVvhP2Uc",
            "thumbnail": "https://img.youtube.com/vi/VtpFVvhP2Uc/0.jpg"
        },
        {
            "title": "PSYCHO",
            "artist": "KORDHELL",
            "genre": "Aggressive Phonk",
            "platform": "youtube",
            "externalID": "bQQAh8tJh8U",
            "thumbnail": "https://img.youtube.com/vi/bQQAh8tJh8U/0.jpg"
        },
        {
            "title": "RAVE",
            "artist": "DXRK ダーク",
            "genre": "House Phonk",
            "platform": "youtube",
            "externalID": "WlXjnPz37sY",
            "thumbnail": "https://img.youtube.com/vi/WlXjnPz37sY/0.jpg"
        },
        {
            "title": "SHADOW LADY",
            "artist": "PORTWAVE",
            "genre": "Vaporwave Phonk",
            "platform": "youtube",
            "externalID": "XmYfF2rInVc",
            "thumbnail": "https://img.youtube.com/vi/XmYfF2rInVc/0.jpg"
        },
        {
            "title": "AUTOMOTIVO BIBI FOGOSA",
            "artist": "Bibi Babydoll",
            "genre": "Brazilian Phonk",
            "platform": "youtube",
            "externalID": "U4Lz5vuwwC4",
            "thumbnail": "https://img.youtube.com/vi/U4Lz5vuwwC4/0.jpg"
        },
        {
            "title": "BLOODY MARY",
            "artist": "Lady Gaga (Phonk Remix)",
            "genre": "Remix Phonk",
            "platform": "youtube",
            "externalID": "gtXwZ1SmlI8",
            "thumbnail": "https://img.youtube.com/vi/gtXwZ1SmlI8/0.jpg"
        }
    ]
    
    try:
        result = await track_collection.insert_many(sample_tracks)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} tracks!")
        print("\nGenres added:")
        genres = set(track["genre"] for track in sample_tracks)
        for genre in sorted(genres):
            count = sum(1 for track in sample_tracks if track["genre"] == genre)
            print(f"  - {genre}: {count} tracks")
        
        print("\n🎉 Database seeding complete!")
        print("You can now start the frontend and backend servers.")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 Phonk Universe - Database Seeder")
    print("=" * 50)
    asyncio.run(seed_tracks())