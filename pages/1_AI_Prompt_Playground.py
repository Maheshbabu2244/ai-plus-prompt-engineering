import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

# --- Page Configuration ---
st.set_page_config(page_title="AI Prompt Playground", page_icon="🚀", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Custom Title Style */
    .stTitle {
        font-weight: 600;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    /* Custom Text Area with Focus Effect */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }

    .stTextArea textarea:focus {
        border-color: #ffffff;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
    }
    
    /* Custom Button Style */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #ffffff;
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.4);
        border-color: #ffffff;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
    }

    /* Card for AI responses */
    .response-card {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        color: white;
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

# This is a 3D animation of a rocket, as requested
LOTTIE_URL = "https://lottie.host/b246995b-59e3-441a-85e8-4012581643c3/g6a5h2BAbp.json"


# --- Model Initialization ---
@st.cache_resource
def get_models():
    models = {}
    try:
        models["GPT-4o (OpenAI)"] = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o")
    except Exception as e: st.warning(f"Could not load OpenAI model.")
    try:
        models["Gemini 1.5 Pro (Google)"] = ChatGoogleGenerativeAI(api_key=st.secrets["GOOGLE_API_KEY"], model="gemini-1.5-pro-latest")
    except Exception as e: st.warning(f"Could not load Gemini model.")
    # The Anthropic model is commented out as per our previous conversation
    # try:
    #     models["Claude 3 Sonnet (Anthropic)"] = ChatAnthropic(api_key=st.secrets["ANTHROPIC_API_KEY"], model_name="claude-3-sonnet-20240229")
    # except Exception as e: st.warning(f"Could not load Claude model.")
    return models

models = get_models()


# --- App Layout ---
st.markdown('<h1 class="stTitle">🚀 AI Prompt Playground</h1>', unsafe_allow_html=True)
st.markdown("<p style='color: white;'>Compare responses from different leading AI models side-by-side.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    prompt = st.text_area("Enter your prompt here:", height=200, placeholder="e.g., Explain the theory of relativity in simple terms.")
    
    if not models:
        st.error("No AI models could be loaded. Please check your API keys.")
    else:
        selected_models = st.multiselect("Choose models to compare:", options=list(models.keys()), default=list(models.keys()))

        if st.button("Generate Responses", type="primary"):
            if not prompt:
                st.warning("Please enter a prompt.")
            elif not selected_models:
                st.warning("Please select at least one model.")
            else:
                with st.spinner("The AIs are thinking..."):
                    cols_responses = st.columns(len(selected_models))
                    for i, model_name in enumerate(selected_models):
                        with cols_responses[i]:
                            st.markdown(f"### {model_name}")
                            try:
                                response = models[model_name].invoke(prompt)
                                st.markdown(f'<div class="response-card">{response.content}</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error: Could not get response.")

with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=400, key="playground_animation")