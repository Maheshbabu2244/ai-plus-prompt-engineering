import streamlit as st
import requests
from streamlit_lottie import st_lottie

# --- Page Configuration ---
st.set_page_config(page_title="AI Learning Hub", page_icon="🤖", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(-45deg, #6a11cb, #2575fc, #ec008c, #fc6767);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        font-family: 'Poppins', sans-serif;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stTitle {
        font-weight: 600;
        color: white;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }
    .stMarkdown h3 {
        color: #f1f1f1 !important;
    }
    .stMarkdown {
        color: #e1e1e1;
    }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

LOTTIE_URL = "https://lottie.host/e589f6d0-e923-43a0-8320-22c293339d37/jV59mET35j.json"
lottie_json = load_lottieurl(LOTTIE_URL)
if lottie_json:
    st_lottie(lottie_json, speed=1, height=350, key="homepage_animation")

# --- Main Page Content ---
st.markdown('<h1 class="stTitle">Welcome to the AI+ Prompt Engineering Hub! 🤖</h1>', unsafe_allow_html=True)
st.markdown("""
This is your one-stop platform for mastering the art and science of prompt engineering. Each module in the sidebar is a powerful tool designed to give you hands-on experience with cutting-edge AI.
### How to Get Started:
1.  **🚀 AI Prompt Playground**: Test a single prompt against multiple LLMs side-by-side.
2.  **👨‍🏫 AI Prompt Coach**: Get AI-powered feedback on your prompts to improve clarity and effectiveness.
3.  **🛠️ Mini Project Builder**: Apply your skills to create practical outputs like LinkedIn bios or resumes.
4.  **📚 Prompt Templates Library**: Explore a curated library of high-quality prompts for various tasks.
5.  **🖼️ AI Image Lab**: Turn your words into images and get feedback on your image prompts.
6.  **🏆 Gamification & Leaderboard**: Participate in weekly challenges and see how you rank against others.
7.  **🤝 Collaboration Hub**: Work on prompt chains in a shared workspace.
8.  **💼 Career & Freelance Tools**: Build your professional documents and practice for interviews.
9.  **🔬 Ethics & Bias Detector**: Analyze your prompts for potential ethical issues and biases.
**Select a tool from the sidebar to begin your journey!**
""")