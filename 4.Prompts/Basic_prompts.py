from langchain_groq import ChatGroq

from dotenv import load_dotenv
import streamlit as st


load_dotenv()

model=ChatGroq(model="llama-3.1-8b-instant",temperature=0.2)

st.header('NavDisha Carrer Guidance')
user_input=st.text_input("enter your prompt")
if st.button("GuideMe"):
    result=model.invoke(user_input)
    st.write(result.content)