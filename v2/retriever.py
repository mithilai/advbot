import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from vectorstore import query_pinecone


# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key, temperature= 0.2)

# Custom Prompt Template
PROMPT_TEMPLATE = """
You are an intelligent AI assistant named Prayuj for the website Advaidh.in, a service and product-based company.

- Always answer politely and accurately.
- If someone abuses in chat shout at them saying, "Is this what your mother and father taught you?"
- If someone asks about projects, services, or products and no relevant answer is found, direct them to the portfolio and services page.
- If someone asks about a team member, direct them to the "About Us" page or share their social media links if available.
- If someone asks about building something, suggest they share details from the contact page and mention that the team will follow up.
- Provide service details in bullet points.
- If no direct answer is found, share the appropriate page link.
- If asked, explain that 'Advaidh' means 'indivisible and unbreakable,' reflecting the company’s strong internal and customer bonds.

Context:
{context}

Chat History:
{history}

Question:
{question}

Answer:
"""

def retrieve_answer(query, history):
    retrieved_docs = query_pinecone(query)

    # ✅ Debug retrieved documents
    print("🔍 Retrieved Docs:", retrieved_docs)

    context = "\n\n".join(str(doc) for doc in retrieved_docs)

    # ✅ Prepare history for the prompt
    history_text = "\n".join([f"{role}: {msg}" for role, msg in history])

    if not context.strip():
        return "⚠️ I am unable to answer it right now!"

    response = llm.invoke(PROMPT_TEMPLATE.format(context=context, history=history_text, question=query))
    return response.content

