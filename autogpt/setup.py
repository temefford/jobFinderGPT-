"""Set up the AI and its goals"""
from colorama import Fore, Style
from autogpt import utils
from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.logs import logger
from utils.upload_resume import main, userPortfolio
import streamlit as st
from streamlit_chat import message
import time
      
cfg = Config()
openai_api = cfg.openai_api_key
google_api = cfg.google_api_key

# --- Initialising SessionState ---
if "ai_name" not in st.session_state:
    st.session_state.ai_name = False
if "ai_role" not in st.session_state:
    st.session_state.ai_role = False
if "ai_goals" not in st.session_state:
    st.session_state.ai_goals = False
    
@st.cache_data(experimental_allow_widgets=True)
def get_name():
    with st.form(key='agent_name', clear_on_submit=True):
        ai_name= st.text_input(
            "**Name Your Agent Here**",
            placeholder="Ari Gold"
            )
        name_button = st.form_submit_button(label='Confirm Name')
    if (name_button and ai_name) or st.session_state.ai_name:
        st.session_state.ai_name = True
        return ai_name

@st.cache_data(experimental_allow_widgets=True)
def get_role():
    with st.form(key='agent_role', clear_on_submit=True):
        ai_role = st.text_area(
                "**Insert AI's Role Here**",
                value="The role of this LLM (Language Model Manager) is to create and manage a chatbot that acts as a job search assistant to help the user find a job."
                "The chatbot is designed to provide various tools and guidance to the user, including finding job posts, writing cover letters, cleaning up the portfolio, "
                "cold emailing, doing research, and sending reminders. The LLM is responsible for training and fine-tuning the chatbot using a large language model, such as "
                "GPT-3.5, to ensure that the chatbot can accurately and effectively assist the user in their job search. The LLM is also responsible for managing the chatbot's "
                "memory, including conversation history and user preferences, to provide a personalized and seamless experience for the user.",
                height=250
                #autocomplete= "an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
                )
        role_button = st.form_submit_button(label=f"**Define agent's Role**")
    if (role_button and ai_role) or st.session_state.ai_role:
        st.session_state.role = True     
        return ai_role
    
@st.cache_data(experimental_allow_widgets=True)
def get_goals():
    with st.form(key='agent_role', clear_on_submit=True):
        ai_goals = st.text_area(
            "**Insert AI's Goals Here**",
            "Improve job search success rates - One of the primary goals of this AI is to help users improve their job search success rates. This can be measured by tracking the number of successful job applications and the percentage of job offers received.",
            "Increase user satisfaction - Another important goal for this AI is to increase user satisfaction. This can be achieved by providing personalized and effective job search assistance, responding quickly to user inquiries, and delivering high-quality recommendations.",
            "Reduce time spent on job searching - Job searching can be a time-consuming process, and the goal of this AI is to help users reduce the amount of time spent searching for jobs. This can be measured by tracking the average time spent on job searches and comparing it to the",
            "time spent when using the AI-powered job search assistant.",
            height=250,
            #autocomplete= "an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
            )    
        goals_button = st.form_submit_button(f"**Confirm agents's Goals**")
    if goals_button and ai_goals and st.session_state.ai_goals:
        return ai_goals

def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object containing the user's input
    """ 
    message("What would you like to name me?")     
    ai_name = get_name()
    if ai_name or st.session_state.ai_name:
        ai_role = get_role()
        if ai_role or st.session_state.ai_role:
            ai_goals = get_goals()
            if ai_goals or st.session_state.ai_goals:
                return AIConfig(ai_name, ai_role, ai_goals)
        
    # container for chat history
    # response_container = st.container()
    # container for text box
    # container = st.container()

    # with container: 
    #     st.subheader("Time to meet your new assistant")
    #     st.write("---")
    #     with st.spinner(
    #         "beeeep"
    #         ):
    #         time.sleep(2) 
   
    #         with st.spinner(
    #                     "Thinnnkinng"
    #                 ):
    #             time.sleep(1) 
    #             # Get AI Role from User
    #             message(f"Hi, I'm {ai_name} and I'll be your personal assistant in all things related to you "
    #                     "getting hired! Let's start with you describing how you'd like me to help you on your job search")
    #             with st.spinner(
    #                             "Thinnnkinng"
    #                         ):
    #                     time.sleep(2) 
    #             message(
    #                 "For example, 'an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications.'",
    #                 )
    #             with st.spinner(
    #                     "Your turn:"
    #                 ):
    #                 time.sleep(3) 
    #             message("...", "you")
                
                
                    


                
