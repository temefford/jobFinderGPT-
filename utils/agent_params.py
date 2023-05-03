import streamlit as st
from streamlit_chat import message
import time

# --- Initialising SessionState ---
if "ai_name" not in st.session_state:
    st.session_state.ai_name = False
if "ai_role" not in st.session_state:
    st.session_state.ai_role = False
if "ai_goals" not in st.session_state:
    st.session_state.ai_goals = False
    
def define_agent():   
    message("What would you like to name me?") 
    with st.form(key='agent_name', clear_on_submit=True):
        ai_name= st.text_input(
            "**Name Your Agent Here**",
            placeholder="Ari Gold"
            )
        name_button = st.form_submit_button(label='Confirm Name')
    if (name_button and ai_name) or st.session_state.ai_name:
        st.session_state.ai_name = ai_name
        message(f"Hi, I'm {ai_name} and I'll be your personal assistant in all things related to you "
                "getting hired! Let's start with you describing how you'd like me to help you on your job search") 
        if name_button and st.session_state.ai_role==False:
            with st.spinner("Thinnkkkinng"):
                time.sleep(1) 
        with st.form(key='agent_role', clear_on_submit=True):
            ai_role = st.text_area(
                "**Insert AI's Role Here**",
                value="The role of this LLM (Language Model Manager) based agent is to create and manage a chatbot that acts as a job search assistant to help the user find a job."
                "The chatbot is designed to provide various tools and guidance to the user, including finding job posts, writing cover letters, cleaning up the portfolio, "
                "cold emailing, doing research, and sending reminders. The LLM is responsible for training and fine-tuning the chatbot using a large language model, such as "
                "GPT-3.5, to ensure that the chatbot can accurately and effectively assist the user in their job search. The LLM is also responsible for managing the chatbot's "
                "memory, including conversation history and user preferences, to provide a personalized and seamless experience for the user.",
                height=250
                #autocomplete= "an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
                )
            role_button = st.form_submit_button(label=f"**Define agent's Role**")
        if (role_button and ai_role) or st.session_state.ai_role:
            st.session_state.ai_role = ai_role
            if not st.session_state.ai_goals:
                with st.spinner("Your turn:"):
                    time.sleep(2)  
            message("Now let me know what specific goals I can help you accomplish!")  
            with st.form(key='agent_goals', clear_on_submit=True):
                ai_goal_1 = st.text_area(
                    "**Insert AI's Goal Here**",
                    value="Help strategize and plan how to get interviews for jobs",
                    height=50
                    )
                ai_goal_2 = st.text_area(
                    "**Insert AI's Goal Here**",
                    value="Finding job posts",
                    height=50
                    ) 
                ai_goal_3 = st.text_area(
                    "**Insert AI's Goal Here**",
                    value="Improving my portfolio",
                    height=50
                    )
                ai_goals = [ai_goal_1, ai_goal_2, ai_goal_3]     
                goals_button = st.form_submit_button(f"**Confirm agents's Goals**")
            if (goals_button and ai_goals) or st.session_state.ai_goals:
                return st.session_state.ai_name, st.session_state.ai_role, ai_goals
                    
# if __name__ == "__main__":
#     define_agent()