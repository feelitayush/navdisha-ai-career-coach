from langchain_huggingface import HuggingFaceEmbeddings


embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
documents=[
    'hello myself ayush',"don't waste your time",'hardwork paysoff'
]
result=embedding.embed_documents(documents)
print(str(result))