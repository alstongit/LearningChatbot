from fastapi import FastAPI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from bson import ObjectId
from llm_utils import qa_chain
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


MONGDODB_URI = os.getenv(MONGDODB_URI)

# MongoDB and LangChain setup
client = MongoClient("MONGODB_URI")
db = client["real_estate"]
collection = db["properties"]

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embedding_model,
    index_name="embedding_index",
    text_key="description"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_properties(query: str):
    try:
        if not query:
            return {"error": "Empty query received"}

        results = vectorstore.similarity_search(query, k=5)

        clean_results = []
        for r in results:
            doc = r.metadata
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            clean_results.append(doc)

        return clean_results

    except Exception as e:
        return {"error": str(e)}

@app.get("/chat")
def chat_response(query: str):
    try:
        if not query:
            return {"error": "Empty query received"}

        # Get top 5 matching docs
        results = vectorstore.similarity_search(query, k=5)
        context = "\n\n".join([r.page_content for r in results])

        # Run LLM chain
        response = qa_chain.run({
            "question": query,
            "context": context
        })

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}
