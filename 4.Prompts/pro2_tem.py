import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate

load_dotenv()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="NavDisha AI Career Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #
def load_css():
    st.markdown("""
    <style>
    /* Background Image with Dark Overlay */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2832&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
 .stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(2,6,23,0.9), rgba(15,23,42,0.85));
    z-index: 0;
}
    
    /* Bring content to front */
    .block-container {
        z-index: 1;
        position: relative;
    }

    /* Enhanced Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
     .glass-card:hover {
    transform: translateY(-5px);
    transition: 0.3s ease;
    box-shadow: 0 10px 40px rgba(0, 198, 255, 0.3);
    }
    /* Gradient Text for Headers */
    .gradient-text {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Primary Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 198, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ---------------- HEADER ---------------- #
st.markdown('<h1 class="gradient-text">🚀 NavDisha AI Career Coach</h1>', unsafe_allow_html=True)
st.markdown("### Build your personalized career roadmap like a pro.")
st.write("---")

# ---------------- SIDEBAR & INPUTS ---------------- #
with st.sidebar:
    st.header("📌 Profile Setup")

    profile_input = st.selectbox("Your Current Status", [
        "Beginner (No experience)",
        "Student (1st-2nd year)",
        "Student (3rd-4th year)",
        "Recent Graduate",
        "Working Professional (Non-Tech)",
        "Working Professional (Tech - Junior Level)"
    ])

    # Custom Target Role Logic
    role_options = [
        "Backend Developer", "Frontend Developer", "Full Stack Developer",
        "Machine Learning Engineer", "Data Scientist", "AI Engineer",
        "DevOps Engineer", "Cloud Engineer", "Cybersecurity Analyst",
        "Software Engineer", "Custom..."
    ]
    selected_role = st.selectbox("🎯 Target Role", role_options)
    
    if selected_role == "Custom...":
        final_role = st.text_input("Enter your target role:", placeholder="e.g. Prompt Engineer")
    else:
        final_role = selected_role

    # Custom Skills Logic
    skills_options_input = st.multiselect("🛠️ Current Skills", [
        "Python","Java","C++","Data Structures","Algorithms","OOP",
        "SQL","HTML/CSS","JavaScript","React","Node.js",
        "Machine Learning","Deep Learning",
        "Data Analysis","Git & GitHub","APIs","Docker",
        "Linux","Problem Solving"
    ])
    
    additional_skills = st.text_input("➕ Any other skills?", placeholder="Comma separated (e.g. AWS, Figma)")
    
    # Combine skills
    final_skills = skills_options_input.copy()
    if additional_skills:
        final_skills.extend([s.strip() for s in additional_skills.split(",") if s.strip()])

    time_duration = st.selectbox("⏳ Roadmap Duration", ["3 Months", "4 Months", "6 Months"])

# ---------------- MODEL & PROMPT ---------------- #
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

# Notice the strict headers (##) so we can parse the output easily
template = PromptTemplate(
    template="""
Act as a Senior Career Coach and Technical Hiring Manager.
Create a highly practical, job-ready roadmap. Do not use generic fluff.

User Profile: {profile}
Target Role: {role}
Current Skills: {skills}
Duration: {duration}

Format your response STRICTLY using these headers:

## 🎯 Insight
(Give a 2-3 sentence reality check on the market for this role and profile).

## 📊 Skills Gap
(List ✅ Existing skills that are useful, and ❌ Missing skills they must learn).

## 📅 Roadmap
(Break this down month by month for {duration}. Format as Month 1:, Month 2:, etc. Include Concepts, Tasks, and Output for each month).

## 🚀 Projects
(Suggest 2 real-world portfolio projects to build).

## 💼 Strategy
(Give actionable tips for Resume, Portfolio, and Interview prep).
""",
    input_variables=["skills", "role", "profile", "duration"]
)

# ---------------- SESSION STATE ---------------- #
if "roadmap_data" not in st.session_state:
    st.session_state.roadmap_data = None

# ---------------- GENERATION LOGIC ---------------- #
if st.button("🚀 Generate My Custom Roadmap"):

    if not final_role:
        st.warning("⚠️ Please specify a target role.")
    elif not final_skills:
        st.warning("⚠️ Please provide at least one skill to start with.")
    else:
        with st.spinner("Analyzing profile and building your roadmap..."):
            prompt = template.invoke({
                "skills": ", ".join(final_skills),
                "role": final_role,
                "profile": profile_input,
                "duration": time_duration
            })

            try:
                result = model.invoke(prompt)
                raw_text = result.content
                
                # Simple parsing logic using regex to split by headers
                sections = re.split(r'(?m)^##\s+', raw_text)
                parsed_data = {"raw": raw_text}
                
                for section in sections:
                    if section.startswith("🎯 Insight"): parsed_data["insight"] = section.replace("🎯 Insight", "").strip()
                    elif section.startswith("📊 Skills Gap"): parsed_data["skills"] = section.replace("📊 Skills Gap", "").strip()
                    elif section.startswith("📅 Roadmap"): parsed_data["roadmap"] = section.replace("📅 Roadmap", "").strip()
                    elif section.startswith("🚀 Projects"): parsed_data["projects"] = section.replace("🚀 Projects", "").strip()
                    elif section.startswith("💼 Strategy"): parsed_data["strategy"] = section.replace("💼 Strategy", "").strip()
                
                st.session_state.roadmap_data = parsed_data
                st.toast("Roadmap Generated Successfully!", icon="✅")

            except Exception as e:
                st.error(f"Error generating roadmap: {e}")

# ---------------- DISPLAY DASHBOARD ---------------- #
if st.session_state.roadmap_data:
    data = st.session_state.roadmap_data
    
    # Top Level Insight Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Coach's Insight")
    st.markdown(data.get("insight", "Insight not found. Check raw output."))
    st.markdown('</div>', unsafe_allow_html=True)

    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["📅 The Timeline", "📊 Skills & Projects", "💼 Career Strategy"])

    with tab1:
        st.markdown("### 🛤️ Your Step-by-Step Roadmap")
        roadmap_text = data.get("roadmap", "")
        
        # Split roadmap text into months to create a visual timeline UI
        months = re.split(r'(?m)^(Month \d+:?)', roadmap_text)
        
        if len(months) > 1:
            for i in range(1, len(months), 2):
                month_title = months[i].replace(":", "").strip()
                month_content = months[i+1].strip() if i+1 < len(months) else ""
                
                # Streamlit 1.30+ has native borders for containers
                with st.container(border=True):
                    st.subheader(f"📌 {month_title}")
                    st.markdown(month_content)
        else:
            # Fallback if LLM formatting fails
            st.markdown(roadmap_text)

    with tab2:
        colA, colB = st.columns(2)
        with colA:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Skill Gap Analysis")
            st.markdown(data.get("skills", ""))
            st.markdown('</div>', unsafe_allow_html=True)
        with colB:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🚀 Portfolio Projects")
            st.markdown(data.get("projects", ""))
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💼 Job Hunt Strategy")
        st.markdown(data.get("strategy", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    # ---------------- ACTION BUTTONS ---------------- #
    col1, col2, col3 = st.columns([1,1,2])
    
    with col1:
        st.download_button(
            label="📥 Download Plan (.txt)",
            data=data.get("raw", ""),
            file_name=f"{final_role.replace(' ', '_')}_Roadmap.txt",
            mime="text/plain"
        )
    with col2:
        if st.button("🔄 Start Over"):
            st.session_state.roadmap_data = None
            st.rerun()