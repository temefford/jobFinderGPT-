import streamlit as st
from autogpt.config import config


# Set up the Streamlit app
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="",
#     layout="centered")
st.subheader("Your Dashboard")
st.markdown("---")
# Main Description
st.markdown("### 👋 Welcome to jobFinderGPT, your best tool to help you get your next job!")
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")

# Set up the sidebar
st.sidebar.markdown(
    """
    ### Steps:
    1. Upload PDF File
    2. Enter Your Secret Key to connect to OpenAI
    3. Strategize and get feedback from your personal jobBot
    4. Deploy your bot in a variety of ways to help you land your next job!

    """
    "___"
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
