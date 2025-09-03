import streamlit as st
import requests
from streamlit_lottie import st_lottie
from diffusers import StableDiffusionPipeline
from PIL import Image
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="AI Image Lab", page_icon="🖼️", layout="wide")

# --- Custom CSS for Advanced UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    /* --- Gradient for this page --- */
    .stApp {
        background: linear-gradient(-45deg, #43cea2, #185a9d, #47a8bd, #2c3e50);
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
    .image-container { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); color: white; text-align: center; }
    .image-container img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

# --- Asset Loading ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

LOTTIE_URL = "https://lottie.host/4e50481b-922a-45c0-b53c-1346999091e3/ZcZk0l977n.json"

# --- Model Initialization ---
@st.cache_resource
def load_stable_diffusion():
    try:
        pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", use_safetensors=True)
        pipe = pipe.to("cpu") # You might want to use "cuda" if you have a GPU
        return pipe
    except Exception as e:
        st.error(f"Error loading Stable Diffusion model: {e}")
        return None

sd_pipeline = load_stable_diffusion()

# --- App Layout ---
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<h1 class="stTitle">🖼️ AI Image Lab</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Generate images from your prompts using Stable Diffusion.</p>", unsafe_allow_html=True)
with col2:
    lottie_json = load_lottieurl(LOTTIE_URL)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="image_lab_animation")

prompt = st.text_area("Enter your image prompt:", height=150, placeholder="e.g., A futuristic cityscape of Bengaluru at night, neon lights, flying vehicles")
negative_prompt = st.text_area("Negative prompt (optional):", height=50, placeholder="e.g., blurry, low quality")
num_inference_steps = st.slider("Number of Steps", min_value=20, max_value=100, value=50)
guidance_scale = st.slider("Guidance Scale", min_value=5.0, max_value=15.0, value=7.5, step=0.5)

if st.button("Generate Image", type="primary", disabled=not sd_pipeline):
    if not prompt:
        st.warning("Please enter a prompt to generate an image.")
    elif sd_pipeline:
        with st.spinner("Generating your image..."):
            try:
                image = sd_pipeline(prompt, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images
                if image and len(image) > 0:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(image, caption="Generated Image")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Could not generate image.")
            except Exception as e:
                st.error(f"Error during image generation: {e}")
    else:
        st.error("Stable Diffusion model not loaded. Check your setup.")