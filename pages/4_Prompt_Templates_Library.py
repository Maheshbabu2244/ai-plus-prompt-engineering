import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Prompt Templates Library", page_icon="📚", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c2e3a);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    /* --- General Styles (reusable) --- */
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); }
    
    /* --- Custom Card for Prompts --- */
    .prompt-card {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        color: white;
        transition: all 0.3s ease;
    }
    .prompt-card:hover {
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    .prompt-card h3 {
        color: #f1f1f1;
    }
    .prompt-card .stCodeBlock {
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/80a316b6-1175-4c07-8809-b1d9774619d8/rO9k060XAa.json"

# --- Data Loading ---
@st.cache_data
def load_prompts():
    data = {
        'Category': ['Marketing', 'Coding', 'Job Search', 'Creative Writing', 'Education'],
        'Title': ['AIDA Copywriting Framework', 'Python Code Explainer', 'Targeted Cover Letter', 'Character Backstory Generator', 'Lesson Plan Creator'],
        'Prompt': [
            'Act as an expert copywriter. Write a product description for [Product Name] using the AIDA (Attention, Interest, Desire, Action) framework. The target audience is [Target Audience]. The key benefits are [List of Benefits].',
            'Act as a senior Python developer and code reviewer. Explain the following code snippet line by line, identify potential bugs or inefficiencies, and suggest a more optimal version.\n\n```python\n[Your Python Code Here]\n```',
            'Act as a professional resume writer and career coach. Write a compelling cover letter for the role of [Job Title] at [Company Name]. My resume highlights are [Your Key Skills/Achievements]. The job description emphasizes [Key Requirements from Job Description]. Tailor the letter to show how my experience aligns perfectly with their needs.',
            'Generate a detailed character backstory for a [Genre, e.g., fantasy] novel. The character is a [Archetype, e.g., reluctant hero] named [Name]. Key traits are [Trait 1, Trait 2]. Include their childhood, a defining traumatic event, and their ultimate motivation.',
            'Create a detailed lesson plan for a 50-minute high school class on [Subject, e.g., the water cycle]. The plan should include learning objectives, required materials, a 10-minute introductory activity, a 25-minute main explanation, and a 15-minute practical exercise or assessment.'
        ]
    }
    return pd.DataFrame(data)

df = load_prompts()

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">📚 Prompt Templates Library</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>A curated collection of high-quality prompts to kickstart your work.</p>", unsafe_allow_html=True)
with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="library_animation")

# --- Filtering and Search ---
search_term = st.text_input("Search prompts...", "")
categories = ['All'] + sorted(df['Category'].unique().tolist())
selected_category = st.selectbox("Filter by category:", categories)

# Apply filters
filtered_df = df
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
if search_term:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(search_term, case=False)]

# --- Display Prompts ---
if filtered_df.empty:
    st.warning("No prompts found with your current filters.")
else:
    for index, row in filtered_df.iterrows():
        st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
        st.markdown(f"### {row['Title']}")
        st.caption(f"Category: {row['Category']}")
        st.code(row['Prompt'], language='text')
        st.markdown('</div>', unsafe_allow_html=True)