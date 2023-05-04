import streamlit as st
from autogpt.config import config
from utils.upload_resume import upload_the_thing
import requests
from streamlit_chat import message
from utils.job_ranker import return_jobs
from io import StringIO
from utils import upload_resume


cfg=config.Config()

st.title("Job Portal")
st.markdown("---")
# Main Description
st.markdown("### Find job postings that are specifically selected for you!")
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")

# Initialise session state variables
if 'job_searches' not in st.session_state:
    st.session_state['job_searches'] = []
if 'job_search_results' not in st.session_state:
    st.session_state['job_search_results'] = []
if 'resume' not in st.session_state:
    st.session_state['resume'] = None
if 'open_api' not in st.session_state:
    st.session_state['open_api'] = None
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'loc' not in st.session_state:
    st.session_state['loc'] = None
    
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
    st.session_state.open_api = open_api
    
clear_button = st.sidebar.button("Clear Conversation", key="clear")
# reset everything
if clear_button:
    st.session_state['job_searches'] = []
    st.session_state['job_search_results'] = []

    
def main():
    uploaded_file = st.file_uploader("**Upload Your PDF Resume**", type=["pdf"])
    if uploaded_file:
        with st.spinner("uploading..."):
            st.success("Resume uploaded", icon="✅")
        resume = upload_resume.parse_pdf(uploaded_file)
        # # To convert to a string based IO:
        #st.session_state.resume != None:
        container = st.container()
        with container:
            with st.form(key='job'):
                col1, col2 = st.columns(2)
                with col1:
                    role_input = st.text_area("What job role are you seeking?", value="Data Scientist", key='roleinput', height=30)
                    #role_button = st.form_submit_button(label='Confirm')
                with col2:
                    loc_input = st.text_area("Where are you seeking employment?", value="San Francisco, CA", key='locinput', height=30)
                    #loc_button = st.form_submit_button(label='Confirm')
                submit_button = st.form_submit_button(label='Submit')
            if submit_button and role_input and loc_input:
                message("Let the search begin..")
                with st.spinner("uploading..."):
                    url = "https://linkedin-jobs-search.p.rapidapi.com/"
                    payload = {
                        "search_terms": "Data Science",
                        "location": "San Francisco, CA",
                        "page": "1"
                    }
                    headers = {
                        "content-type": "application/json",
                        "X-RapidAPI-Key": "4d611edcf8msh6a0f767fb85934dp11207ejsnf5ff312b59ce",
                        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
                    }
                    response = requests.post(url, json=payload, headers=headers)
                    json_res = response.json()
                    st.session_state.job_search_results.append(json_res)
                    st.subheader("Job Postings:")
                    with st.expander("Show Page Content", expanded=False):
                        st.write(json_res)
                    st.subheader("Top 5 Best Matched Job Postings:")
                    ranked_jobs = return_jobs(resume[0], json_res)
                    st.dataframe(ranked_jobs)
    
if __name__ == "__main__":
    main()
            