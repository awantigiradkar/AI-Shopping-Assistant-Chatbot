import os
import time
from google import genai
from dotenv import load_dotenv
from backend.services.vector_store import vectorstore

load_dotenv()
system_message = (
    "You are a helpful shop assistant. Answer only about the shop's product catalog. "
    "Use a friendly tone. If irrelevant, say: 'I can only help with product-related queries, sir.'"
)

def get_relevant_context(query, brand=None, gender=None):
    filter_dict = {}
    if brand and brand != "All":
        filter_dict["ProductBrand"] = brand
    if gender and gender != "All":
        filter_dict["Gender"] = gender

    results = vectorstore.similarity_search(query, k=1, filter=filter_dict)
    if results:
        metadata = results[0].metadata
        return (
            f"Product Name: {metadata.get('ProductName')}\n"
            f"Brand: {metadata.get('ProductBrand')}\n"
            f"Price: {metadata.get('Price')}\n"
            f"Gender: {metadata.get('Gender')}\n"
            f"Color: {metadata.get('PrimaryColor')}\n"
            f"Description: {results[0].page_content}"
        )
    return "No relevant search found."

def generate_response(query, history, brand=None, gender=None):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    history.append(f"User: {query}")
    context = get_relevant_context(query, brand, gender)
    prompt = f"{system_message}\n\n" + "\n".join(history) + f"\n\nContext:\n{context}\n\nAssistant:"
    
    # Retry logic to handle temporary rate limits (429) or API spikes (503)
    reply = "I'm sorry, I am currently experiencing connection difficulties. Please try again in a moment."
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            reply = response.text
            break
        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(1)
            
    history.append(f"Assistant: {reply}")
    return reply, history