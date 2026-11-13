import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="meta-llama/llama-4-maverick",
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
        max_tokens=1000  
    ) 