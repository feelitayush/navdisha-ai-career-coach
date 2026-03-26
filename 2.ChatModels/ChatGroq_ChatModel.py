from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",   # working model
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    
)

response = model.invoke(
    "u are a career guide act as my mentor a senior data scientist i am interested in becoming ai engineer  i have completed python basics suggest me a structured learning path 6 month phase one plan"
)

print(response.content)