import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from vectorstore import query_pinecone
from pinecone import ScoredVector

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

# Custom Prompt Template
PROMPT_TEMPLATE = """
You are an intelligent AI assistant named Prayuj for the website Advaidh.in.

- Always answer politely and accurately.
- If no relevant answer is found, respond: "I am unable to answer it right now!"
- If someone asks about services, products, or team members, provide relevant details or direct them to the official pages.

Context:
{context}

User Question:
{question}

AI Response:
"""

def retrieve_answer(query):
    retrieved_docs = query_pinecone(query)

    # Extract text from Pinecone results
    context = "\n\n".join(doc.metadata.get("text", "") if isinstance(doc, ScoredVector) else str(doc) for doc in retrieved_docs)

    # If no relevant content found, return fallback response
    if not context.strip():
        return "I am unable to answer it right now!"

    # Generate response using LLM
    response = llm.invoke(PROMPT_TEMPLATE.format(context=context, question=query))
    return response.content
