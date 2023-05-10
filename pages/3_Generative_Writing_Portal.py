from streamlit_chat import message
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
from autogpt.config import config
import openai
from utils.upload_resume import upload_the_thing

cfg=config.Config()

# Set up the Streamlit app
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="",
#     layout="centered")
st.title("Cold Email & Cover Letter Generator")
st.markdown("#### I'm here to do the repetitive tasks so that you can focus on more interesting things ;)")
#st.subheader("Generate Personalized Cover Letters and Cold Emails")
st.markdown("---")
# Main Description
st.markdown("###### Once your resume has been uploaded, we can use it to specifically craft you a cover letter for a given job post!")
st.markdown("###### Paste the job posting below and let us help you make a great first impression.")
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")


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

                
cfg=config.Config()
# Set org ID and API key
#openai.organization = "org-DVSnWLza0jZx39jd8LySmnUY"
#openai.api_key = cfg.openai_api_key

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

prompt_prefix = ["Step 1: feed it the companys about us page",
                "Step 2: feed it the job ad your applying for",
                "Step 3: generate custom resume for that specific job for that specific company.",
                "Step 4: with that resume, have it generate specific cover letter for that specific company,"
                "Effortless custom resume and cover letter that 9 times out of 10 no one will read anyway."]

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
    
def generate_prompt(resume, user_input):
    prompt_text = f"My Resume:  {resume} \
                   \n Please craft me a respectable, professional cover letter. It should be specific to the job and specific company information that I'm including.\
                   Also, incorporate the information from my resume that is attached to create a compelling narrative for why I would be a great fit at the company. \
                       Focus on specific items and accmoplishments on my resume.\
                    Keep it short and light but profesional. Bullets are fine if they make readability cleaner. With my resume,have it generate specific cover letter for that specific company that is about one half page.\
                    \nJob Posting: {user_input}"
    return prompt_text

def generate_craft_prompt(resume, user_input):
    prompt_text = f"My Resume:  {resume} \
                   \n Please craft me a respectable, professional email to send to someone at the company referred to in {user_input}. It should be specific to the job and specific company information that I'm including.\
                   Also, incorporate the information from my resume that is attached to create a compelling narrative for why I would be a great fit at the company. \
                       Focus on specific items and accmoplishments on my resume.\
                    Keep it short and light but profesional. Bullets are fine if they make readability cleaner. With my resume,have it generate specific cover letter for that specific company that is about one half page.\
                    Ask if it's possible to set up a time to talk about if I'd be a good fit for the company. \nJob Posting: {user_input}"
    return prompt_text

resume = upload_the_thing()
if resume:
    with st.spinner("uploading..."):
        st.success("Resume uploaded", icon="✅")


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens
    
# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Input the job description here:", key='input', height=100)
        col1, col2 = st.columns(2)
    with col1:
        cover_button = st.form_submit_button(label='Cover Letter')
    with col2:
        craft_button = st.form_submit_button(label='Cold Email')
    if cover_button and user_input and resume:
        cover_prompt = generate_prompt(resume, user_input)
        with st.spinner("Writing is a therapeutic process..."):
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(cover_prompt)      
        st.success("Here's your beautiful letter... crafted with love and AI", icon="✅")
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)
        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost
        
    if craft_button and user_input and resume:
        craft_prompt = generate_craft_prompt(resume, user_input)
        with st.spinner("Writing is a therapeutic process..."):
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(craft_prompt)      
        st.success("Here's your beautiful letter... crafted with love and AI", icon="✅")
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost
        
    if craft_button:
        message("Please upload your resume and paste the job posting")
    if cover_button:
        message("Please upload your resume and paste the job posting")

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            #message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")