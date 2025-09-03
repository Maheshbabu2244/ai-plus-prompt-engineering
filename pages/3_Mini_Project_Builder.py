import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI
from docx import Document
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="Mini Project Builder", page_icon="🛠️", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #f7971e, #ffd200, #f5af19, #f12711);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    /* --- General Styles (reusable) --- */
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); transition: all 0.3s ease; }
    .stTextArea textarea:focus, .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within { border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .stButton>button { border-radius: 20px; border: 1px solid #ffffff; background-color: rgba(255, 255, 255, 0.2); color: white; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: rgba(255, 255, 255, 0.4); border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .main-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# --- Lottie for this page ---
LOTTIE_URL = "https://lottie.host/17a8b0c8-2b89-4886-8889-2cc35141b714/g3d2FJy6jG.json"

# --- LLM Initialization ---
try:
    llm = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.7)
except Exception as e:
    st.error("Failed to initialize the language model. Please check your API key.")
    st.stop()

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">🛠️ Mini Project Builder</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Apply your prompt skills to generate useful documents and code.</p>", unsafe_allow_html=True)
with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="builder_animation")

project_options = ["LinkedIn 'About' Section", "Code Docstring Generator", "Short Story Idea"]
selected_project = st.selectbox("Choose a mini-project:", project_options)

# Use the custom container class for the main content area
st.markdown('<div class="main-container">', unsafe_allow_html=True)

if selected_project == "LinkedIn 'About' Section":
    st.subheader("LinkedIn Bio Generator")
    with st.form("linkedin_form"):
        role = st.text_input("Your Role/Profession", "e.g., Senior Data Scientist")
        skills = st.text_input("Key Skills/Technologies (comma-separated)", "e.g., Python, Machine Learning, TensorFlow")
        tone = st.selectbox("Tone", ["Professional", "Enthusiastic", "Story-telling"])
        submitted = st.form_submit_button("Generate Bio")

        if submitted:
            prompt = f"Generate a compelling LinkedIn 'About' section for a {role}. Key skills to highlight are: {skills}. The desired tone is {tone}. The bio should be 3 paragraphs long, engaging, and end with a call-to-action to connect."
            with st.spinner("Crafting your professional story..."):
                response = llm.invoke(prompt).content
                st.text_area("Generated Bio:", response, height=300)
                
                doc = Document()
                doc.add_paragraph(response)
                bio = BytesIO()
                doc.save(bio)
                st.download_button("Download as DOCX", bio.getvalue(), "linkedin_bio.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

elif selected_project == "Code Docstring Generator":
    st.subheader("Python Docstring Generator")
    with st.form("docstring_form"):
        code_snippet = st.text_area("Paste your Python function here:", height=200, placeholder="def my_function(param1, param2):")
        submitted = st.form_submit_button("Generate Docstring")
        
        if submitted:
            prompt = f"Act as a senior Python developer. Generate a professional Google-style docstring for the following Python function. The docstring should include a summary, arguments (Args), and what it returns (Returns).\n\nFunction:\n```python\n{code_snippet}\n```"
            with st.spinner("Generating documentation..."):
                response = llm.invoke(prompt).content
                st.code(response, language='python')

elif selected_project == "Short Story Idea":
    st.subheader("Short Story Idea Generator")
    with st.form("story_form"):
        genre = st.text_input("Genre", "e.g., Sci-Fi, Fantasy, Mystery")
        character = st.text_input("Main Character Archetype", "e.g., Reluctant Hero, Jaded Detective")
        setting = st.text_input("Setting", "e.g., A cyberpunk Bengaluru, An ancient forgotten temple")
        submitted = st.form_submit_button("Generate Idea")

        if submitted:
            prompt = f"Generate three unique and intriguing short story ideas. Each idea should be a single paragraph. The story must be in the {genre} genre, feature a {character} as the main character, and take place in a setting like {setting}."
            with st.spinner("Brewing up some creative ideas..."):
                response = llm.invoke(prompt).content
                st.text_area("Generated Story Ideas:", response, height=400)

st.markdown('</div>', unsafe_allow_html=True)