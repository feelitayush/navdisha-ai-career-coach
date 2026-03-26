from langchain_huggingface import ChatHuggingFace , HuggingFacePipeline

llm=HuggingFacePipeline.from_model_id(
    model_id='model id to be downloaded ',
    task='text-generation',
    pipeline_kwargs=dict( temperature=0.5 , max_new_token=100)
)
model=ChatHuggingFace(llm=llm)
result=model.invoke("query to be asked here")
print(result.content)