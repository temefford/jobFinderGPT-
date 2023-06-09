"""
This is the main page, that you have to run with "streamlit run main.py" to launch the app locally.
Streamlit automatically create the tabs in the left sidebar from the .py files located in /pages
Here we just have the home page, with a short description of the tabs, and some images
"""
from autogpt.config import config
import streamlit as st

cfg=config.Config()
# Set up the Streamlit app

st.set_page_config(
    page_title="JobFinderGPT",
    page_icon="👋",
    layout="centered")
st.title("Job Finder GPT")
st.subheader("Finding a job shouldn't be your full-time job. It's ours.")
st.markdown("\n --- \n")
# Main Description
st.markdown("### 👋 Welcome to jobFinderGPT, your best tool to help you get your next job!")
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")

# Set up the sidebar
st.markdown(
    """
    ### Steps:
    1. Upload PDF File
    2. Enter Your Secret Key to connect to OpenAI
    3. Enter Your other API keys for access to agents with internet search capability and persistant storage.
    4. Strategize and get feedback from your personal jobBot
    5. Deploy your bot in a variety of ways to help you land your next job!

    """
    "___"
)

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
    
# serp_api = st.sidebar.text_input(
#     "**Enter SERP API Key**",
#     type="password",
#     placeholder="sk-",
#     help="https://platform.openai.com/account/api-keys",
# )  
# if serp_api:
#     cfg.set_serp_api_key(serp_api)
#     st.write("SERPAPI stored")

google_api = st.sidebar.text_input(
    "**Enter Google API Key**",
    type="password",
    placeholder="",
    help="https://platform.openai.com/account/api-keys",
)  
if google_api:
    cfg.set_google_api_key(google_api)
    st.sidebar.write("Google API stored")
    
pinecone_api = st.sidebar.text_input(
    "**Enter Pinecone API Key**",
    type="password",
    placeholder="",
    help="https://platform.openai.com/account/api-keys",
)  
if pinecone_api:
    cfg.set_pinecone_api_key(pinecone_api)
    st.sidebar.write("Pinecone API stored")
    
pinecone_region = st.sidebar.text_input(
    "**Enter Pinecone Region**",
    type="password",
    placeholder="",
    help="https://platform.openai.com/account/api-keys",
)  
if pinecone_region:
    cfg.set_pinecone_region(pinecone_region)
    st.sidebar.write("Pinecone Region stored")
    

   
st.sidebar.markdown("---")
st.markdown("---")

st.subheader("Our Job Bot Agent is here to help you land your next job. Let's start by looking at your resume so that our AI can better understand how they can be of service.")

