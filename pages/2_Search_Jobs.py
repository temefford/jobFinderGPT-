import streamlit as st
from autogpt.config import config
from utils.upload_resume import upload_the_thing

cfg=config.Config()

# Set up the Streamlit app
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="",
#     layout="centered")
st.title("Job Portal")
st.markdown("---")
# Main Description
st.markdown("### Find job postings that are specifically selected for you!")
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")

resume = upload_the_thing()
if resume:
    with st.spinner("uploading..."):
        st.success("Resume uploaded", icon="✅")
        
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