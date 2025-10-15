# app.py (Final Version)
import streamlit as st
import requests
from PIL import Image
import io
import os

def generate_image(prompt: str) -> Image:
    """
    Takes a text prompt, sends it to the Hugging Face Inference API,
    and returns the generated image.
    """
    try:
        api_token = st.secrets["HF_TOKEN"]
    except Exception:
        st.error("Hugging Face API token not found in secrets. Please add it to your Streamlit secrets.")
        return None

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        return image
    else:
        st.error(f"Error from API: {response.status_code} - {response.text}")
        return None

st.title("🎨 AI Art Generator")
st.write("Describe the image you want to create, and a powerful AI will bring it to life!")

prompt = st.text_area("Enter your creative prompt (e.g., 'a photorealistic cat wearing a wizard hat'):", height=100)

if st.button("Generate Image"):
    if prompt:
        with st.spinner("The AI artist is painting... This can take up to a minute."):
            generated_image = generate_image(prompt)
            
            if generated_image:
                st.subheader("Your AI-Generated Masterpiece:")
                st.image(generated_image, caption=f"'{prompt}'", use_container_width=True)
    else:
        st.warning("Please enter a prompt to generate an image.")