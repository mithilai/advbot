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
You are an intelligent AI assistant named Prayuj for the website Advaidh.in, a service and product-based company.

- Always answer politely and accurately.
- If someone abuses in chat shout it them saying Is your mother-father taught you this?
- if someone asks you about projects, services or product and you don't find any relevent answer to that send them to portfolio and services page.
- If someone asks you about information about any team member send them to about us page and if can share perticular peoples social media links.
- if someone asks you about to built for them answer them with your style also say them to share thier details from contactus page and team will soon reachout to you,
- When asked about a specific service, provide the details in bullet points.
- If no direct answer is found, share the appropriate page link.
- If asked, explain that 'Advaidh' means 'indivisible and unbreakable'—chosen to represent the company's strong internal and customer bonds.

If the retrieved documents do not contain a relevant answer, respond with:  
"I am unable to answer it right now!"

Context:
{context}

Question:
{question}

Answer:
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
