import streamlit as st
import os
import time
import pandas as pd
import json
from dotenv import load_dotenv

# API client libraries
import openai
import google.generativeai as genai
from groq import Groq
import requests

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="ModelMind | 5-Way LLM Comparison",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    body { color: #cccccc; background-color: #0a0a0a; } .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { color: #ffffff; }
    .stButton>button { border-radius: 12px; background-image: linear-gradient(135deg, #00ff88 0%, #00ccff 100%); color: #0a0a0a; border: none; padding: 1rem 2rem; font-weight: 700; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
    .stTextArea textarea { background-color: #1a1a1a; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid rgba(255, 255, 255, 0.1); }
    [data-testid="stMetric"] { background-color: #1a1a1a; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- API Key Loading ---
def load_key(key_name):
    try: return st.secrets[key_name]
    except (KeyError, FileNotFoundError): return None

openai_api_key = load_key("OPENAI_API_KEY")
google_api_key = load_key("GOOGLE_API_KEY")
groq_api_key = load_key("GROQ_API_KEY")
hf_api_key = load_key("HUGGINGFACE_API_KEY")
deepseek_api_key = load_key("DEEPSEEK_API_KEY") # Added DeepSeek key

# --- Performance Tracking Wrapper ---
def track_performance(api_func):
    def wrapper(model, prompt, temperature):
        start_time = time.monotonic()
        first_token_time = None
        full_response = ""
        try:
            for content_chunk in api_func(model, prompt, temperature):
                if first_token_time is None: first_token_time = time.monotonic()
                full_response += content_chunk
                yield content_chunk
        except Exception as e:
            yield f"Error: {str(e)}"
        finally:
            end_time = time.monotonic()
            total_time = end_time - start_time
            ttft = first_token_time - start_time if first_token_time else 0
            yield {
                "done": True, "total_time": total_time, "ttft": ttft,
                "output_chars": len(full_response),
                "chars_per_second": len(full_response) / total_time if total_time > 0 else 0
            }
    return wrapper

# --- Model API Functions ---
@track_performance
def get_openai_response(model, prompt, temperature):
    client = openai.OpenAI(api_key=openai_api_key)
    stream = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=temperature, stream=True)
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content: yield content

@track_performance
def get_google_gemini_response(model, prompt, temperature):
    genai.configure(api_key=google_api_key)
    model_instance = genai.GenerativeModel(model)
    stream = model_instance.generate_content(prompt, stream=True, generation_config=genai.types.GenerationConfig(temperature=temperature))
    for chunk in stream:
        if chunk.text: yield chunk.text

@track_performance
def get_groq_response(model, prompt, temperature):
    client = Groq(api_key=groq_api_key)
    stream = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=temperature, stream=True)
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content: yield content

@track_performance
def get_hf_response(model, prompt, temperature):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    data = {"inputs": prompt, "parameters": {"temperature": max(0.1, temperature)}, "stream": True}
    response = requests.post(API_URL, headers=headers, json=data, stream=True)
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith('data:'):
                try:
                    chunk = json.loads(line_str.lstrip('data:'))
                    content = chunk.get('token', {}).get('text', '')
                    if content: yield content
                except (json.JSONDecodeError, KeyError): continue

@track_performance
def get_deepseek_response(model, prompt, temperature):
    """New function for DeepSeek API (OpenAI compatible)."""
    client = openai.OpenAI(
        api_key=deepseek_api_key,
        base_url="https://api.deepseek.com/v1"
    )
    stream = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=temperature, stream=True)
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content: yield content

# --- Model Definitions ---
ALL_MODELS = {
    "OpenAI GPT-4o": {"func": get_openai_response, "args": {"model": "gpt-4o"}, "key": openai_api_key},
    "Google Gemini 1.5 Pro": {"func": get_google_gemini_response, "args": {"model": "gemini-1.5-pro-latest"}, "key": google_api_key},
    "Llama 3 70B (Groq)": {"func": get_groq_response, "args": {"model": "llama3-70b-8192"}, "key": groq_api_key},
    "Mistral 7B (Hugging Face)": {"func": get_hf_response, "args": {"model": "mistralai/Mistral-7B-Instruct-v0.2"}, "key": hf_api_key},
    "DeepSeek Chat": {"func": get_deepseek_response, "args": {"model": "deepseek-chat"}, "key": deepseek_api_key},
}
AVAILABLE_MODELS = {name: details for name, details in ALL_MODELS.items() if details["key"]}

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Model Configuration")
    st.markdown("Models will only appear if their API key is in your secrets file.")
    if not AVAILABLE_MODELS:
        st.error("No API keys found! Please add at least one key to your secrets file.")
    
    selected_models = st.multiselect("Choose models to compare:", options=list(AVAILABLE_MODELS.keys()), default=list(AVAILABLE_MODELS.keys()))
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, help="Controls randomness.")

# --- Main App Interface ---
st.title("🧠 5-Way LLM Comparison")
st.markdown("### Compare outputs from five leading AI model APIs.")

prompt = st.text_area("Enter your prompt here:", height=150, placeholder="e.g., Explain the theory of relativity in simple terms")

if st.button("Generate Responses"):
    if not prompt: st.warning("Please enter a prompt.")
    elif not selected_models: st.warning("Please select at least one available model.")
    else:
        all_metrics = {}
        cols = st.columns(len(selected_models))
        
        for i, model_name in enumerate(selected_models):
            with cols[i]:
                st.subheader(model_name)
                text_placeholder, metrics_placeholder = st.empty(), st.empty()
                full_response = ""
                model_info = AVAILABLE_MODELS[model_name]
                api_func, model_args = model_info["func"], model_info["args"]
                
                with st.spinner("Generating..."):
                    response_generator = api_func(prompt=prompt, temperature=temperature, **model_args)
                    for chunk in response_generator:
                        if isinstance(chunk, dict) and chunk.get("done"):
                            all_metrics[model_name] = chunk
                            metrics_placeholder.info(f"**TTFT:** {chunk['ttft']:.2f}s | **Total:** {chunk['total_time']:.2f}s | **T/s:** {chunk['chars_per_second']:.2f}")
                        else:
                            full_response += chunk
                            text_placeholder.markdown(full_response + " ▌")
                text_placeholder.markdown(full_response)
        
        # --- Final Performance Summary ---
        if all_metrics:
            st.markdown("---")
            st.header("📊 Performance Comparison")
            df = pd.DataFrame.from_dict(all_metrics, orient='index').drop(columns=['done'])
            df.rename(columns={'ttft': 'Time to First Token (s)', 'total_time': 'Total Time (s)', 'output_chars': 'Output Characters', 'chars_per_second': 'Throughput (chars/s)'}, inplace=True)
            st.dataframe(df.style.format("{:.2f}").highlight_min(subset=['Time to First Token (s)', 'Total Time (s)'], color='#00686b').highlight_max(subset=['Output Characters', 'Throughput (chars/s)'], color='#00686b'), use_container_width=True)
            
            st.subheader("🏆 Category Winners")
            c1, c2, c3 = st.columns(3)
            best_ttft, best_throughput, best_total_time = df['Time to First Token (s)'].idxmin(), df['Throughput (chars/s)'].idxmax(), df['Total Time (s)'].idxmin()
            c1.metric("⚡ Fastest Response (TTFT)", best_ttft, f"{df.loc[best_ttft, 'Time to First Token (s)']:.2f} s")
            c2.metric("🚀 Highest Throughput", best_throughput, f"{df.loc[best_throughput, 'Throughput (chars/s)']:.2f} chars/s")
            c3.metric("⏱️ Shortest Total Time", best_total_time, f"{df.loc[best_total_time, 'Total Time (s)']:.2f} s")