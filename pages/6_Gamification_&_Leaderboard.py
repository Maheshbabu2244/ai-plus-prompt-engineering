import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import random

# --- Page Configuration ---
st.set_page_config(page_title="Gamification & Leaderboard", page_icon="🏆", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #ff9966, #ff5e62, #c94b4b, #43cea2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    /* --- General Styles --- */
    .stTitle { font-weight: 600; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .stTextInput input { border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(255, 255, 255, 0.1); color: white; backdrop-filter: blur(10px); }
    .stTextInput input:focus { border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .stButton>button { border-radius: 20px; border: 1px solid #ffffff; background-color: rgba(255, 255, 255, 0.2); color: white; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: rgba(255, 255, 255, 0.4); border-color: #ffffff; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
    .leaderboard-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; }
    .leaderboard-container table { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/532c5c81-ff2b-4607-9144-096455c0714f/Q01j7JGYNq.json"

# --- Dummy Gamification Logic ---
if 'user_points' not in st.session_state:
    st.session_state['user_points'] = 0
if 'leaderboard_data' not in st.session_state:
    st.session_state['leaderboard_data'] = pd.DataFrame({
        'User': ['AI Enthusiast 1', 'Prompt Master', 'Code Whisperer'],
        'Points': [150, 220, 180]
    }).sort_values(by='Points', ascending=False).reset_index(drop=True)

weekly_challenge = "Write a creative prompt that generates a short story about a street dog in Bengaluru who discovers a hidden talent."
challenge_reward = 20

def submit_prompt(prompt):
    if prompt:
        st.session_state['user_points'] += challenge_reward
        new_entry = pd.DataFrame({'User': ['You'], 'Points': [st.session_state['user_points']]})
        st.session_state['leaderboard_data'] = pd.concat([st.session_state['leaderboard_data'], new_entry], ignore_index=True)
        st.session_state['leaderboard_data'] = st.session_state['leaderboard_data'].sort_values(by='Points', ascending=False).reset_index(drop=True)
        st.success(f"Your prompt was submitted! You earned {challenge_reward} points.")
    else:
        st.warning("Please enter a prompt for the challenge.")

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">🏆 Gamification & Leaderboard</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Participate in challenges and track your progress on the leaderboard.</p>", unsafe_allow_html=True)
    st.subheader("🏆 Weekly Prompt Challenge")
    st.info(f"**Challenge:** {weekly_challenge} (Reward: {challenge_reward} points)")
    challenge_prompt = st.text_area("Submit your prompt here:", height=100)
    st.button("Submit Challenge Prompt", on_click=submit_prompt, args=[challenge_prompt], type="primary")
    st.subheader("Your Progress")
    st.markdown(f"<p style='color: white;'>Your Current Points: <span style='font-weight: bold;'>{st.session_state['user_points']}</span></p>", unsafe_allow_html=True)

with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=250, key="gamification_animation")
    st.subheader("🏆 Leaderboard")
    st.markdown('<div class="leaderboard-container">', unsafe_allow_html=True)
    st.dataframe(st.session_state['leaderboard_data'])
    st.markdown('</div>', unsafe_allow_html=True)