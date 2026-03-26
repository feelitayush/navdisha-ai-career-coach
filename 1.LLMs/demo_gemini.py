from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv 
import os

load_dotenv
api_key=os.getenv("GOOGLE_API_KEY")
print(ap)

model=ChatGoogleGenerativeAI(model='gemini-1.5-flash',google_api_key=api_key)

response=model.invoke("steve jobs connecting dot story")
print(response)