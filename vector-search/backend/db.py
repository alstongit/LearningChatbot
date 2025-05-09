from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, Query
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Load the sentence transformer model (you can swap to mistral if needed later)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

MONGODB_URI = os.getenv(MONGODB_URI)
# Connect to MongoDB (replace with your actual connection string)
client = MongoClient("MONGODB_URI")
db = client["real_estate"]
collection = db["properties"]

# Fetch documents where embedding is missing or null
properties = collection.find({
    "$or": [
        {"embedding": {"$exists": False}},
        {"embedding": None}
    ]
})

count = 0

for prop in properties:
    print(f"Processing property ID: {prop['_id']}")
    try:
        # Generate embedding from description
        embedding = model.encode(prop["description"]).tolist()

        # Update document with embedding
        result = collection.update_one(
            {"_id": prop["_id"]},
            {"$set": {"embedding": embedding}}
        )

        print(f"Updated - Matched: {result.matched_count}, Modified: {result.modified_count}")
        count += 1
    except Exception as e:
        print(f"❌ Error processing property ID {prop['_id']}: {e}")

print(f"\n✅ Total properties updated with embeddings: {count}")


