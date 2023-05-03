from colorama import Fore, Style

from autogpt.app import execute_command, get_command
from autogpt.chat import chat_with_ai, create_chat_message
from autogpt.config import Config
from autogpt.json_utils.json_fix_llm import fix_json_using_multiple_techniques
from autogpt.json_utils.utilities import validate_json
from autogpt.logs import logger, print_assistant_thoughts
from autogpt.speech import say_text
from autogpt.spinner import Spinner
from autogpt.utils import clean_input
import streamlit as st
import time
from streamlit_chat import message
import openai


class Agent:
    """Agent class for interacting with Auto-GPT.

    Attributes:
        ai_name: The name of the agent.
        memory: The memory object to use.
        full_message_history: The full message history.
        next_action_count: The number of actions to execute.
        system_prompt: The system prompt is the initial prompt that defines everything the AI needs to know to achieve its task successfully.
        Currently, the dynamic and customizable information in the system prompt are ai_name, description and goals.

        triggering_prompt: The last sentence the AI will see before answering. For Auto-GPT, this prompt is:
            Determine which next command to use, and respond using the format specified above:
            The triggering prompt is not part of the system prompt because between the system prompt and the triggering
            prompt we have contextual information that can distract the AI and make it forget that its goal is to find the next task to achieve.
            SYSTEM PROMPT
            CONTEXTUAL INFORMATION (memory, previous conversations, anything relevant)
            TRIGGERING PROMPT

        The triggering prompt reminds the AI about its short term meta task (defining the next task)
    """

    def __init__(
        self,
        ai_name,
        memory,
        full_message_history,
        next_action_count,
        system_prompt,
        triggering_prompt,
    ):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.system_prompt = system_prompt
        self.triggering_prompt = triggering_prompt
        
            
    def start_interaction_loop(self):
        # Interaction Loop
        cfg = Config()
        command_name = None
        arguments = None
        user_input = ""
        #message("Start Agent?")
        st.subheader("Now entering into work mode... Results will be posted below:")
        st.markdown("---")
        # Initialise session state variables
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        if "user_input" not in st.session_state:
            st.session_state['user_input'] = ""
        if "output" not in st.session_state:
            st.session_state['output'] = ""

        # generate a response
        def generate_response(prompt):
            st.session_state['messages'].append({"role": "user", "content": prompt})

            with st.spinner(
                "Analyzing your goals and forming a plan... `{}` ".format("Thinking very very hard")
                ):     
                    assistant_reply = chat_with_ai(
                    self.system_prompt,
                    self.triggering_prompt,
                    self.full_message_history,
                    self.memory,
                    cfg.fast_token_limit,
                )  # TODO: This hardcodes the model to use GPT3.5. Make this an argument

            assistant_reply_json = fix_json_using_multiple_techniques(assistant_reply)
            command_name, arguments = get_command(assistant_reply_json)
            if command_name:
                response = assistant_reply
                st.session_state['messages'].append({"role": "assistant", "content": response})
                return response

        # container for chat history
        response_container = st.container()
        # container for text box
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input(f"- Enter 'yes' to authorise command, \n"
                    "- 'Exit' to exit program \n - or enter your own feedback for me execute", value="yes", key='input')
                submit_button = st.form_submit_button(label='Send')
            if submit_button and user_input:
                st.session_state['user_input'] = user_input
                output = generate_response(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
                if user_input.lower().strip() == "yes":
                    user_input = "GENERATE NEXT COMMAND JSON"
                    message("I'll keep on working...")
                    result = (
                        f"Command {command_name} returned: "
                        f"{execute_command(command_name, arguments)}"
                    )
                    if self.next_action_count > 0:
                        self.next_action_count -= 1
                    memory_to_add = (
                        f"Assistant Reply: {output} "
                        f"\nResult: {result} "
                        f"\nHuman Feedback: {user_input} "
                    )
                    self.memory.add(memory_to_add)
                    if result is not None:
                        self.full_message_history.append(create_chat_message("system", result))
                else:  
                    command_name = "human_feedback"
                    message(
                        "NEXT ACTION: ",
                        f"COMMAND = {command_name}",
                        f"  ARGUMENTS = {arguments}",
                    )
                    result = f"Human feedback: {user_input}"
                    memory_to_add = (
                        f"Assistant Reply: {output} "
                        f"\nResult: {result} "
                        f"\nHuman Feedback: {user_input} "
                    )
                    self.memory.add(memory_to_add)
                    # Check if there's a result from the command append it to the message
                    # history
                    if result is not None:
                        #self.full_message_history.append(create_chat_message("system", result))
                        st.write("SYSTEM: ", result)
                    else:
                        self.full_message_history.append(
                            create_chat_message("system", "Unable to execute command")
                        )
                        logger.typewriter_log(
                            "SYSTEM: ", Fore.YELLOW, "Unable to execute command"
                        )

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))
