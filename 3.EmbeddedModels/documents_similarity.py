from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
documents=[ "Artificial Intelligence enables machines to simulate human intelligence by learning from data, recognizing patterns, and making decisions autonomously.", 
           "Cybersecurity focuses on protecting systems, networks, and data from unauthorized access, attacks, and vulnerabilities through encryption and security protocols.",
"Data Science involves extracting meaningful insights from structured and unstructured data using statistical methods, machine learning, and data visualization techniques.",
"Software Engineering is the systematic approach to designing, developing, testing, and maintaining reliable and scalable software ",
"Cloud Computing provides on-demand access to computing resources like storage and servers over the internet, enabling scalability and cost-effective solutions."]

query="i am learning machine learning teach me about this field"

query_embedding=embeddings.embed_query(query)
documents_embeddings=embeddings.embed_documents(documents)

scores=cosine_similarity([query_embedding],documents_embeddings)[0]
index,score= sorted(list(enumerate(scores)),key=lambda x: x[1])[-1]
print(query)
print(documents[index])
print("similarity score is :",score)