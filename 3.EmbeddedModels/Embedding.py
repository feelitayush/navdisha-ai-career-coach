from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv

text='hello i am ayush i am ready to become better version of my'
embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector=embedding.embed_query(text)

print(str(vector))