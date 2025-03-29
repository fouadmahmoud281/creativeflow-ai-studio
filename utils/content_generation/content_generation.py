import streamlit as st
from together import Together
import time
import base64
import requests
from io import BytesIO

def generate_text(prompt, model=None):
    """
    Generate text content using TogetherAI's API
    
    Args:
        prompt (str): The prompt for text generation
        model (str, optional): Model name. If None, uses the session's default model.
    
    Returns:
        str: Generated text content or None if an error occurs
    """
    if not st.session_state.api_key:
        st.error("Please enter your Together AI API key in the settings tab.")
        return None
    
    if model is None:
        model = st.session_state.get("default_text_model", "deepseek-ai/DeepSeek-V3")
    
    try:
        with st.spinner("Generating text..."):
            # Initialize Together client
            client = Together(api_key=st.session_state.api_key)
            
            # Call the API
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            
            # Extract the generated text
            return response.choices[0].message.content
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def generate_image(prompt, model=None, width=1024, height=1024):
    """
    Generate image content using TogetherAI's API
    
    Args:
        prompt (str): The prompt for image generation
        model (str, optional): Model name. If None, uses the session's default model.
        width (int): Output image width
        height (int): Output image height
    
    Returns:
        str: Base64 encoded image data or None if an error occurs
    """
    if not st.session_state.api_key:
        st.error("Please enter your Together AI API key in the settings tab.")
        return None
    
    if model is None:
        model = st.session_state.get("default_image_model", "stabilityai/stable-diffusion-xl-base-1.0")
    
    headers = {
        "Authorization": f"Bearer {st.session_state.api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": 50,
        "seed": int(time.time()) % 1000000
    }
    
    try:
        with st.spinner("Generating image..."):
            response = requests.post(
                "https://api.together.xyz/v1/images/generations",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_json = response.json()
                
                if "data" in response_json and len(response_json["data"]) > 0:
                    image_data = response_json["data"][0]
                    
                    # Check if the response contains a URL
                    if "url" in image_data:
                        # Download the image from the URL
                        image_url = image_data["url"]
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            # Convert the downloaded image to base64
                            image_bytes = BytesIO(img_response.content)
                            base64_image = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
                            return base64_image
                        else:
                            st.error(f"Failed to download image from URL: {image_url}")
                            return None
                    else:
                        st.error(f"No image URL found in response. Available keys: {list(image_data.keys())}")
                        return None
                else:
                    st.error("No data found in the API response")
                    return None
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
                return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None
