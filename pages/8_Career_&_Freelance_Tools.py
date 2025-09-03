import streamlit as st
import requests
from streamlit_lottie import st_lottie
from langchain_openai import ChatOpenAI

# --- Page Configuration ---
st.set_page_config(page_title="Career & Freelance Tools", page_icon="💼", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #cc2b5e, #753a88, #4286f4, #373b44);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    /* --- General Styles --- */
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextArea textarea, .stTextInput input, .stSelectbox div { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); }
    .stTextArea textarea:focus, .stTextInput input:focus, .stSelectbox div:focus-within { border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .stButton>button { border-radius: 20px; border: 1px solid #ffffff; background-color: rgba(255, 255, 255, 0.2); color: white; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: rgba(255, 255, 255, 0.4); border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .tool-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/8e1856d7-f140-450d-a637-71798119d399/o6VlqU6mF6.json"

# --- LLM Initialization ---
try:
    llm = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.6)
except Exception as e:
    st.error("Failed to initialize the language model. Please check your API key.")
    st.stop()

# --- Interview Q&A Logic ---
if 'interview_question' not in st.session_state:
    st.session_state['interview_question'] = ""
if 'interview_feedback' not in st.session_state:
    st.session_state['interview_feedback'] = ""

interview_topics = ["Behavioral", "Technical", "Situational"]

def generate_interview_question(topic):
    if topic == "Behavioral":
        questions = [
            "Tell me about a time you failed.",
            "Describe a situation where you had to work with a difficult team member.",
            "Tell me about a time you had to learn something quickly.",
        ]
    elif topic == "Technical":
        questions = [
            "Explain the concept of prompt engineering.",
            "What are the benefits of using virtual environments in Python?",
            "Describe the difference between generative and discriminative AI models.",
        ]
    elif topic == "Situational":
        questions = [
            "How would you approach a project with a very tight deadline?",
            "Imagine a client is unhappy with the results of your work. How would you handle this?",
            "Describe how you would explain AI to someone with no technical background.",
        ]
    return random.choice(questions) if questions else "No questions available for this topic."

def get_feedback(answer, question):
    prompt = f"Provide constructive feedback on the following interview answer to the question: '{question}'. The answer is: '{answer}'. Focus on clarity, conciseness, and relevance. Suggest improvements if necessary."
    try:
        response = llm.invoke(prompt).content
        st.session_state['interview_feedback'] = response
    except Exception as e:
        st.error(f"Error getting feedback: {e}")

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">💼 Career & Freelance Tools</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Prepare for your career with AI-powered tools and practice.</p>", unsafe_allow_html=True)

    st.subheader("💬 Interview Q&A Simulator")
    selected_topic = st.selectbox("Choose an interview question type:", interview_topics)
    if st.button("Generate Question", type="primary"):
        st.session_state['interview_question'] = generate_interview_question(selected_topic)
    if st.session_state['interview_question']:
        st.info(f"**Question:** {st.session_state['interview_question']}")
        interview_answer = st.text_area("Your Answer:", height=150)
        st.button("Get Feedback", on_click=get_feedback, args=[interview_answer, st.session_state['interview_question']], type="primary")
        if st.session_state['interview_feedback']:
            st.subheader("Feedback:")
            st.markdown(f'<div class="tool-container"><pre style="white-space: pre-wrap;">{st.session_state["interview_feedback"]}</pre></div>', unsafe_allow_html=True)

    st.subheader("✍️ Resume & Cover Letter Review (Coming Soon)")
    st.info("This feature will allow you to upload your resume and cover letter for AI-powered feedback.")

with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=300, key="career_animation")