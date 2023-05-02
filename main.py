from autogpt.cli import main
from autogpt.config import config
from autogpt.pages import upload_resume
import streamlit as st
import os




# Set up the Streamlit app
st.title("Job Finder GPT")
st.subheader("Finding a job shouldn't be your full-time job. It's ours.")

# Set up the sidebar
st.sidebar.markdown(
    """
    ### Steps:
    1. Upload PDF File
    2. Enter Your Secret Key for Embeddings
    3. Perform Q&A

    **Note : File content and API key not stored in any form.**
    """
)

# Allow the user to enter an OpenAI API key
api = st.sidebar.text_input(
    "**Enter OpenAI API Key**",
    type="password",
    placeholder="sk-",
    help="https://platform.openai.com/account/api-keys",
)
if api:
    config.set_openai_api_key(api)
    
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []

# if 'past' not in st.session_state:
#     st.session_state['past'] = []
  
with st.container():
    upload_resume.main()

with st.container():
    st.subheader("Our Job Bot Agent is here to help you land your next job")
    main()
