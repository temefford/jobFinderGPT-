import streamlit as st
from autogpt.config import config
cfg=config.Config()

# Set up the Streamlit app
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="",
#     layout="centered")
st.subheader("Your Dashboard")
st.markdown("---")
# Main Description
st.markdown("### 👋 Welcome to jobFinderGPT, your best tool to help you get your next job!")


# Allow the user to enter an OpenAI API key
open_api = st.sidebar.text_input(
    "**Enter OpenAI API Key**",
    type="password",
    placeholder="sk-",
    help="https://platform.openai.com/account/api-keys",
)  
if open_api:
    cfg.set_openai_api_key(open_api)
    st.sidebar.write("**OpenAPI stored**")
    
google_api = st.sidebar.text_input(
    "**Enter Google API Key**",
    type="password",
    placeholder="",
    help="https://platform.openai.com/account/api-keys",
)  
if google_api:
    cfg.set_google_api_key(google_api)
    st.sidebar.write("Google API stored")
