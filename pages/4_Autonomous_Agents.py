"""Set up the AI and its goals"""
from colorama import Fore, Style
from autogpt import utils
from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.logs import logger
from utils.upload_resume import main, userPortfolio
from autogpt.agent.agent import Agent
import streamlit as st
from streamlit_chat import message
from utils.agent_params import define_agent
from autogpt.prompt import construct_prompt
from autogpt.configurator import create_config
from autogpt.logs import logger
from autogpt.memory import get_memory
from utils.upload_resume import side_upload_the_thing
import time
      

# --- Initialising SessionState ---
if "ai_name" not in st.session_state:
    st.session_state.ai_name = False
if "ai_role" not in st.session_state:
    st.session_state.ai_role = False
if "ai_goals" not in st.session_state:
    st.session_state.ai_goals = False
      
cfg = Config()
openai_api = cfg.openai_api_key
google_api = cfg.google_api_key
st.title("Your Personal Employment Agency")
st.subheader("Set up and manage your team of AI bots to help you find a job. The 'job agents' that are recursively trained as you interact with them and are attached to LLM's and the internet to do the tedious work for you.")
st.markdown("\n --- \n")

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

# Initialise session state variables
if 'generated_team' not in st.session_state:
    st.session_state['generated_team'] = []
if 'past_team' not in st.session_state:
    st.session_state['past_team'] = []
if 'messages_team' not in st.session_state:
    st.session_state['messages_team'] = [
        {"role_team": "system", "content_team": "You are a helpful assistant."}
    ]
if 'model_name_team' not in st.session_state:
    st.session_state['model_name_team'] = []
if 'cost_team' not in st.session_state:
    st.session_state['cost_team'] = []
if 'total_tokens_team' not in st.session_state:
    st.session_state['total_tokens_team'] = []
if 'total_cost_team' not in st.session_state:
    st.session_state['total_cost_team'] = 0.0
if 'open_api' not in st.session_state:
    st.session_state['open_api'] = None
if 'memory' not in st.session_state:
    st.session_state['memory'] = []

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.write("---")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost_team']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")
st.sidebar.write("---")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated_team'] = []
    st.session_state['past_team'] = []
    st.session_state['messages_team'] = [
        {"role_team": "system", "content_team": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens_team'] = []
    st.session_state['model_name_team'] = []
    st.session_state['cost_team'] = []
    st.session_state['total_cost_team'] = 0.0
    st.session_state['total_tokens_team'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost_team']:.5f}")

res_upload = st.sidebar.button("Upload Resume")
if res_upload:
    resume = side_upload_the_thing()
    if resume:
        with st.spinner("uploading..."):
            st.success("Resume uploaded", icon="✅")

st.subheader("Time to meet your new assistant")
st.write("---")
    
def main():
    agent_params = define_agent()
    if agent_params:
        message("yayyyy")
        ai_name, ai_role, ai_goals = agent_params
        st.session_state.ai_name, st.session_state.ai_role, st.session_state.ai_goals = ai_name, ai_role, ai_goals
        system_prompt = construct_prompt(ai_name, ai_role, ai_goals)
        if system_prompt:
            # Initialize variables
            full_message_history = []
            next_action_count = 0
            # Make a constant:
            triggering_prompt = (
                "Determine which next command to use, and respond using the"
                " format specified above. If your responses are too similar to previous than this prompt should be registered as 'create a prompt to advance my progress toward giving good advice about job hunting.':"
            )
            openai_api = st.text_input(
                "**Enter Your OpenAI API Key**",
                type="password",
                placeholder="sk-",
                help="https://platform.openai.com/account/api-keys",
            )  
            if openai_api:
                cfg.set_openai_api_key(openai_api)
                st.write("**OpenAPI stored**")
                # Initialize memory and make sure it is empty.
                # this is particularly important for indexing and referencing pinecone memory
                memory = get_memory(cfg, init=True)
                if memory:
                    # logger.typewriter_log(
                    #     "Using memory of type:", Fore.GREEN, f"{memory.__class__.__name__}"
                    # )
                    # logger.typewriter_log("Using Browser:", Fore.GREEN, cfg.selenium_web_browser)
                    config = AIConfig.load(cfg.ai_settings_file)
                    if config:
                        agent = Agent(
                            ai_name=config.ai_name,
                            memory=memory,
                            full_message_history=full_message_history,
                            next_action_count=next_action_count,
                            system_prompt=system_prompt,
                            triggering_prompt=triggering_prompt,
                        )
                        if agent:
                            agent.start_interaction_loop()  
                        
if __name__ == "__main__":
    main()
            

            
