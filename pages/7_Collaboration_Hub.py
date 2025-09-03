import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI

# --- Page Configuration ---
st.set_page_config(page_title="Collaboration Hub", page_icon="🤝", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #00b09b, #96c93d, #4568dc, #b06ab3);
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
    .chain-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/69059723-a89c-4d99-b99c-785889c3e09c/l4VpXFohs8.json"

# --- LLM Initialization ---
try:
    llm = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.5)
except Exception as e:
    st.error("Failed to initialize the language model. Please check your API key.")
    st.stop()

# --- Session State for Prompt Chain ---
if 'prompt_chain' not in st.session_state:
    st.session_state['prompt_chain'] = []
if 'chain_output' not in st.session_state:
    st.session_state['chain_output'] = ""

def add_step():
    st.session_state['prompt_chain'].append(st.session_state.new_prompt)
    st.session_state.new_prompt = ""

def execute_chain():
    full_prompt = ""
    outputs = []
    with st.spinner("Executing the prompt chain..."):
        for i, prompt in enumerate(st.session_state['prompt_chain']):
            if i > 0:
                full_prompt += f"\n\nBased on the previous output: {outputs[-1]}\n\n"
            full_prompt += f"Step {i+1}: {prompt}"
            try:
                response = llm.invoke(full_prompt).content
                outputs.append(response)
            except Exception as e:
                st.error(f"Error in step {i+1}: {e}")
                return
    st.session_state['chain_output'] = "\n\n".join([f"Step {i+1} Output:\n{output}" for i, output in enumerate(outputs)])

def clear_chain():
    st.session_state['prompt_chain'] = []
    st.session_state['chain_output'] = ""

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">🤝 Collaboration Hub</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Simulate collaborative prompt engineering by building and executing prompt chains.</p>", unsafe_allow_html=True)

    st.subheader("Build Your Prompt Chain")
    st.text_input("Enter a prompt step:", key="new_prompt")
    st.button("Add Step to Chain", on_click=add_step, type="primary")

    if st.session_state['prompt_chain']:
        st.subheader("Current Prompt Chain:")
        for i, prompt in enumerate(st.session_state['prompt_chain']):
            st.markdown(f'<div class="chain-container"><strong>Step {i+1}:</strong> {prompt}</div>', unsafe_allow_html=True)
        st.button("Execute Full Chain", on_click=execute_chain, type="primary")
        st.button("Clear Chain", on_click=clear_chain)

    if st.session_state['chain_output']:
        st.subheader("Chain Output:")
        st.markdown(f'<div class="chain-container"><pre style="white-space: pre-wrap;">{st.session_state["chain_output"]}</pre></div>', unsafe_allow_html=True)

with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=300, key="collaboration_animation")