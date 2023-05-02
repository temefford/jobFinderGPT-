import streamlit as st
import time
from autogpt.cli import main
from streamlit_chat import message
from autogpt.agent.agent import Agent
from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.prompt import construct_prompt
from autogpt.logs import logger
from autogpt.memory import get_memory
from autogpt.config import config
import os

cfg = Config()
st.title("Automic Agent Job Bot")
st.subheader("Get a recurively trained agent attached to LLM's and the internet to do the dirty work for you")
st.markdown("\n --- \n")
# Main Description
#st.markdown("Developed by Theo Mefford: https://github.com/temefford")
#st.markdown("The app is still under development. Please reach me in the github repo if you have any comments or suggestions.")

api = os.getenv('OPENAI_API_KEY')



config = AIConfig.load(cfg.ai_settings_file)
memory = get_memory(cfg, init=True)
full_message_history = []
next_action_count = 0
# Make a constant:
triggering_prompt = (
    "Determine which next command to use, and respond using the"
    " format specified above:"
)

agent_1 = Agent(
    ai_name=config.ai_name,
    memory=memory,
    full_message_history=full_message_history,
    next_action_count=next_action_count,
    system_prompt=construct_prompt(),
    triggering_prompt=triggering_prompt,
    )

agent_1.start_interaction_loop() 
     
main()