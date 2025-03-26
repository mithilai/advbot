import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Load Pinecone API credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# ✅ Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# ✅ Initialize Embeddings Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def add_to_pinecone(docs):
    """Stores documents in Pinecone with embeddings."""
    if not docs:
        print("⚠️ No documents to store.")
        return None

    # ✅ Convert scraped data into LangChain Document objects
    documents = [
        Document(
            page_content=doc["content"], 
            metadata={"source": doc["url"], "content": doc["content"]}
        )
        for doc in docs
    ]

    # ✅ Split documents using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    # ✅ Check if index exists, otherwise create it
    if PINECONE_INDEX not in [index['name'] for index in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=768,  # Match with embedding model dimensions
            metric="cosine"
        )

    # ✅ Connect to the index
    index = pc.Index(PINECONE_INDEX)

    # ✅ Convert documents to embeddings and store in Pinecone
    vectors = []
    for i, doc in enumerate(split_docs):
        embedding = embeddings.embed_query(doc.page_content)
        vectors.append((str(i), embedding, doc.metadata))  # Ensure embedding is a list of floats

    # ✅ Upsert vectors into Pinecone
    index.upsert(vectors)

    print("✅ Data successfully stored in Pinecone.")
    return index


def query_pinecone(query, top_k=3):
    """Retrieve top-k relevant documents from Pinecone."""
    # ✅ Connect to the index
    index = pc.Index(PINECONE_INDEX)

    # ✅ Generate embedding for the query
    embedding = embeddings.embed_query(query)

    # ✅ Ensure query vector is correctly formatted (list of floats)
    if not isinstance(embedding, list) or not all(isinstance(x, (float, int)) for x in embedding):
        raise ValueError("❌ Query embedding must be a list of floats or integers.")

    # ✅ Query Pinecone with correct vector format
    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )

    # ✅ Debug: Check Pinecone query results
    print("🔍 Pinecone Results:", results)

    if not results or "matches" not in results or not results["matches"]:
        print("⚠️ No matches found in Pinecone!")
        return []

    return [Document(page_content=match["metadata"].get("content", "")) for match in results["matches"]]
