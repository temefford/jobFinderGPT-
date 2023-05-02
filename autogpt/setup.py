"""Set up the AI and its goals"""
from colorama import Fore, Style
from autogpt import utils
from autogpt.config.ai_config import AIConfig
from autogpt.logs import logger
from pages.upload_resume import main, userPortfolio
import streamlit as st
from streamlit_chat import message
import time
      
def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object containing the user's input
    """
    with st.spinner(
        "beeeep"
        ):
        time.sleep(2) 
    st.subheader("Time to meet your new assistant")
    st.write("---")
    message("What's your name?")
    user_name= st.text_input(
        "**Your Name Here**",
        placeholder="The Boss"
    )
    if user_name:  
        job_seeker = userPortfolio(name=user_name)
        # Get AI Name from User
        message("....", "you")
        time.sleep(1) 
        ai_name= st.text_input(
            "**Name Your Agent Here**",
            placeholder="Ari Gold"
            )
        if ai_name:
            with st.spinner(
                        "Thinnnkinng"
                    ):
                time.sleep(1) 
                # Get AI Role from User
                message(f"Hi, I'm {ai_name} and I'll be your personal assistant in all things related to you "
                        "getting hired! Let's start with you describing how you'd like me to help you on your job search")
                with st.spinner(
                                "Thinnnkinng"
                            ):
                        time.sleep(2) 
                message(
                    "For example, 'an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications.'",
                    )
                with st.spinner(
                        "Your turn:"
                    ):
                    time.sleep(3) 
                message("...", "you")
                ai_role = st.text_area(
                        "**Insert AI's Role Here**",
                        value="The role of this LLM (Language Model Manager) is to create and manage a chatbot that acts as a job search assistant to help the user find a job."
                        "The chatbot is designed to provide various tools and guidance to the user, including finding job posts, writing cover letters, cleaning up the portfolio, "
                        "cold emailing, doing research, and sending reminders. The LLM is responsible for training and fine-tuning the chatbot using a large language model, such as "
                        "GPT-3.5, to ensure that the chatbot can accurately and effectively assist the user in their job search. The LLM is also responsible for managing the chatbot's "
                        "memory, including conversation history and user preferences, to provide a personalized and seamless experience for the user.",
                        height=250,
                        #autocomplete= "an AI designed to help me clean up my portfolio, write cover letters, and search put forward great applications."
                    )
                with st.spinner(
                        "you're going to keep me busy aren't you...."
                    ):
                    time.sleep(3) 
                role_button = st.button(f"**Define {ai_name}'s Role**")
                if role_button:
                    ai_role = "Welcome to your job search assistant! Your primary goal is to help the user find a job by providing them with the necessary tools and guidance. Your role involves various tasks such as finding job posts, writing cover letters, cleaning up the portfolio, cold emailing, doing research, and sending reminders. Here's what each task entails:",
                    "1. Finding job posts - As a job search assistant, your primary task is to help the user find suitable job postings. This involves searching various job boards, identifying potential opportunities, and presenting them to the user for review.",
                    "2. Writing cover letters - A good cover letter can significantly improve the user's chances of getting hired. As an assistant, you will help the user write an effective cover letter that highlights their skills and experiences.",
                    "3. Cleaning up portfolio - Before applying for a job, it's essential to ensure that the user's portfolio is up-to-date and presents them in the best light possible. You will help the user clean up their portfolio by identifying areas that need improvement and providing suggestions for improvement.",
                    "4. Cold emailing - In addition to applying for job postings, it's also important to reach out to potential employers directly. You will help the user craft professional cold emails that are targeted towards specific companies and individuals.",
                    "5. Doing research - As a job search assistant, you will help the user research potential employers and job postings. This includes conducting company research, identifying key contacts, and learning more about the application process.",
                    "6. Sending reminders - Job searching can be a time-consuming process, and it's easy to forget about deadlines and follow-ups. You will help the user stay on track by sending reminders for important tasks and deadlines.",
                    "In summary, your role as a job search assistant is to help the user find a job by providing them with various tools and guidance. You will assist with tasks such as finding job posts, writing cover letters, cleaning up the portfolio, cold emailing, doing research, and sending reminders. Good luck, and happy job hunting!",

                    # message("Enter up to 5 specific goals for your AI:\n")
                    ai_goals = "Improve job search success rates - One of the primary goals of this AI is to help users improve their job search success rates. This can be measured by tracking the number of successful job applications and the percentage of job offers received.",
                    "Increase user satisfaction - Another important goal for this AI is to increase user satisfaction. This can be achieved by providing personalized and effective job search assistance, responding quickly to user inquiries, and delivering high-quality recommendations.",
                    "Reduce time spent on job searching - Job searching can be a time-consuming process, and the goal of this AI is to help users reduce the amount of time spent searching for jobs. This can be measured by tracking the average time spent on job searches and comparing it to the",
                    "time spent when using the AI-powered job search assistant."
                    for i in range(2):
                        time.sleep(1) 
                    continue_butt = st.button("Ready to Continue?")
                    if continue_butt:
                        return AIConfig(ai_name, ai_role, ai_goals)


                    
