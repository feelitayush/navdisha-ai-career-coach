from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate
load_dotenv()

model=ChatGroq(model="llama-3.1-8b-instant",temperature=0.2)
st.header("NavDisha ElevateU Carrer Guidance ")


profile_input = st.selectbox("Enter your current profile",[
    "Beginner (No experience)",
    "Student (1st-2nd year)",
    "Student (3rd-4th year)",
    "Recent Graduate",
    "Working Professional (Non-Tech)",
    "Working Professional (Tech - Junior Level)"
])


job_roles_input= st.selectbox("Select role you want to learn",[
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Machine Learning Engineer",
    "Data Scientist",
    "AI Engineer",
    "DevOps Engineer",
    "Cloud Engineer",
    "Cybersecurity Analyst",
    "Software Engineer"
])


skills_options_input = st.selectbox("select additional skill you have",[
    "Python",
    "Java",
    "C++",
    "Data Structures",
    "Algorithms",
    "OOP (Object-Oriented Programming)",
    "SQL",
    "HTML/CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Machine Learning Basics",
    "Deep Learning Basics",
    "Data Analysis (Pandas, NumPy)",
    "Git & GitHub",
    "APIs (REST)",
    "Docker Basics",
    "Linux Basics",
    "Problem Solving",
    "Communication Skills"
])

#template 

template=PromptTemplate(
    template="""
You are an expert AI Technology Career Advisor. Your goal is to provide a structured, practical, and time-based career roadmap.

You will receive:
- User's current skills :{skills_options_input}
- Target job role :{job_roles_input}
- Current profile (student / beginner / working professional): {profile_input}

---

Your task:

1. Analyze the user's profile and identify the most relevant career path (aligned with target role).

2. Perform skill gap analysis:
   - Identify matched skills (already known)
   - Identify missing skills (required for the role)

3. Create a structured roadmap:
   - Must be time-based (phases or months)
   - Must include:
     • Concepts to learn  
     • Tools/technologies  
     • Projects to build  
     • Expected outcomes  

4. Provide final preparation strategy:
   - Resume guidance  
   - Portfolio/project strategy  
   - Interview preparation focus   """,
input_variables=['skills_options_input','job_roles_input','profile_input']
)
# fill the placeholders
prompt=template.invoke({
    "skills_options_input":skills_options_input,
    'job_roles_input':job_roles_input,
    'profile_input':profile_input
})


if st.button("Guide Me"):
    result=model.invoke(prompt)
    st.write(result.content)
