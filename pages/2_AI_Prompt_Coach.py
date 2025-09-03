import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="AI Prompt Coach", page_icon="👨‍🏫", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(-45deg, #00c6ff, #0072ff, #3a7bd5, #00d2ff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextArea textarea { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); transition: all 0.3s ease; }
    .stTextArea textarea:focus { border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .stButton>button { border-radius: 20px; border: 1px solid #ffffff; background-color: rgba(255, 255, 255, 0.2); color: white; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: rgba(255, 255, 255, 0.4); border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .response-card { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; margin-top: 1rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; }
    .response-card table { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/5788d57d-f4d0-466d-88b5-3037f69427b2/pS92yJe36u.json"

# --- LLM and Prompt ---
try:
    coach_llm = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.3)
except Exception:
    st.error("Could not initialize the coach model. Check your OpenAI API key.")
    st.stop()

COACH_SYSTEM_PROMPT = "..." # Same system prompt as before

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">👨‍🏫 AI Prompt Coach</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Get instant feedback on your prompts to improve their effectiveness.</p>", unsafe_allow_html=True)
with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="coach_animation")

user_prompt = st.text_area("Enter the prompt you want to evaluate:", height=150)
if st.button("Evaluate My Prompt", type="primary"):
    if not user_prompt:
        st.warning("Please enter a prompt to evaluate.")
    else:
        with st.spinner("Your coach is evaluating the prompt..."):
            messages = [{"role": "system", "content": COACH_SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}]
            try:
                response = coach_llm.invoke(messages)
                st.markdown(f'<div class="response-card">{response.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")