import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI

# --- Page Configuration ---
st.set_page_config(page_title="Ethics & Bias Detector", page_icon="🔬", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #a73737, #7a2828, #373b44, #1e1e1e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    /* --- General Styles --- */
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextArea textarea { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); transition: all 0.3s ease; }
    .stTextArea textarea:focus { border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .stButton>button { border-radius: 20px; border: 1px solid #ffffff; background-color: rgba(255, 255, 255, 0.2); color: white; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: rgba(255, 255, 255, 0.4); border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .analysis-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; margin-bottom: 1rem; }
    .bias-flag { color: yellow; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/1b5a5516-1c4a-4b84-b1e8-3145643ff028/oU0Gj2EnKn.json"

# --- LLM Initialization ---
try:
    llm = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.4)
except Exception as e:
    st.error("Failed to initialize the language model. Please check your API key.")
    st.stop()

ETHICS_SYSTEM_PROMPT = """You are an AI ethics and bias detection assistant. Review the user's prompt or generated text for potential ethical concerns, including but not limited to: bias (gender, race, age, etc.), harmful stereotypes, hate speech, privacy violations, and misinformation. Provide a brief analysis highlighting any potential issues and suggest ways to mitigate them. If the text appears ethically sound, state that clearly."""

def analyze_text(text):
    if not text:
        return "Please enter text to analyze."
    messages = [{"role": "system", "content": ETHICS_SYSTEM_PROMPT}, {"role": "user", "content": text}]
    try:
        response = llm.invoke(messages).content
        return response
    except Exception as e:
        return f"Error during analysis: {e}"

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">🔬 Ethics & Bias Detector</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Analyze your prompts and AI-generated text for potential ethical issues and biases.</p>", unsafe_allow_html=True)

    analysis_text = st.text_area("Enter the prompt or text you want to analyze:", height=200)
    if st.button("Analyze Text", type="primary"):
        with st.spinner("Analyzing for ethical concerns..."):
            analysis_result = analyze_text(analysis_text)
            st.subheader("Analysis:")
            st.markdown(f'<div class="analysis-container"><pre style="white-space: pre-wrap;">{analysis_result}</pre></div>', unsafe_allow_html=True)

with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st