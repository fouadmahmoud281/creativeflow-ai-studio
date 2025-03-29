import streamlit as st

def initialize_session_state():
    """
    Initialize the session state variables if they don't exist
    """
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if 'default_text_model' not in st.session_state:
        st.session_state.default_text_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    
    if 'default_image_model' not in st.session_state:
        st.session_state.default_image_model = "stabilityai/stable-diffusion-xl-base-1.0"