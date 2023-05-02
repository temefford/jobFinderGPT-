"""Set up the AI and its goals"""
from colorama import Fore, Style

from autogpt import utils
from autogpt.config.ai_config import AIConfig
from autogpt.logs import logger
import streamlit as st
from streamlit_chat import message
      
def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object containing the user's input
    """
    # Get AI Name from User
    ai_name= st.text_input(
        "**Name Your Agent Here**",
        placeholder="Ari Gold"
    )
    #ent_button = st.button("Enter")
    #if ent_button:
    #    ai_name = "Ari Gold"
    if ai_name:
        # Get AI Role from User
        message(f"Hi, I'm {ai_name} and I'll be your personal assistant in all things related to you "
                "getting hired! Let's start with you describing how you'd like me to help you on your job search")
        message(
            "For example, 'an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications.'",
        )
        ai_role = st.text_input(
            "**Insert AI's Role Here**",
            placeholder="an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
        )
        # role_button = st.button("Use Example role")
        # print(ai_role)
        # if role_button:
        #     print(4)
        #     ai_role = "an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
        if ai_role:
            message("Enter up to 5 goals for your AI:\n"
                "For example: \n 1 - Increase net worth\n 2 - Grow Twitter Account \n 3 - Develop and manage"
                " multiple businesses autonomously'",
            )
            ai_goals = []
            c = st.container()
            i= 1
            goal1 = st.text_input(
                f"**Goal 1**",
                placeholder="Insert Goal"
            )
            if goal1:
                ai_goals.append(goal1)
                c.write(f"Goal 1: {goal1}")
                goal2 = st.text_input(
                    f"**Goal 2**",
                    placeholder="Insert Goal"
                )   
                if goal2:
                    ai_goals.append(goal2)
                    c.write(f"Goal 2: {goal2}")
                    goal3 = st.text_input(
                        f"**Goal 3**",
                        placeholder="Insert Goal"
                    )   
                    if goal3:
                        ai_goals.append(goal3)
                        c.write(f"Goal 3: {goal3}")
                        goal4 = st.text_input(
                            f"**Goal 4**",
                            placeholder="Insert Goal"
                        )   
                        if goal4:
                            ai_goals.append(goal4)
                            c.write(f"Goal 4: {goal4}")
                            goal5 = st.text_input(
                                f"**Goal 5**",
                                placeholder="Insert Goal"
                            )   
                            if goal5:
                                ai_goals.append(goal4)
                                c.write(f"Goal 5: {goal5}")     
                                message("Great, let's get cracking!")
                                return AIConfig(ai_name, ai_role, ai_goals)       
                cont_button = st.button("Done adding goals. Let's get started")
                if cont_button:
                    message("Great, let's get cracking!")
                    return AIConfig(ai_name, ai_role, ai_goals)


                
