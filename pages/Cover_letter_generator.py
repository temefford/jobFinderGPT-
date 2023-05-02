import openai
import streamlit as st
from streamlit_chat import message
from autogpt.config import config

# Setting page title and header
st.set_page_config(page_title="Cover Letter Generator", page_icon=":robot_face:")
st.title("Cover Letter Generator")
st.markdown("I'm here to do the repetetive tasks so that you can focus on more interesting things ;)")

my_resume = "Theo Mefford\
                San Francisco, CA Phone: (510)381-1534 Email: TheoMefford@gmail.com Webpage: TheoMefford.com\
                LinkedIn: linkedin.com/in/temefford Github: github.com/temefford\
                Education\
                University of San Francisco\
                Masters Program in Data Science June 2023\
                Masters in Business Administration Expected 2024\
                University of Maryland, College Park 2018\
                M.S. in Physics\
                Santa Clara University 2013\
                B.S. in Physics and Mathematics Magna Cum Laude, Blockus Award as the SCU Outstanding Physics Senior\
                Experience\
                Data Science Intern - AgMonitor November 2022 - Present\
                ■ Contributed to the development of a software module that utilizes satellite data and simulation models to predict crop stress.\
                Software Development - vRad/USF August 2021 - January 2023\
                ■ Worked as a researcher through USF in consultation with vRad to build a discrete event simulator that models their network,\
                resulting in low cost experimentation and optimization of their routing algorithm.\
                Data Science Intern - Phylagen January 2021 - April 2021\
                ■ Utilized machine learning models to classify samples of microbial relative abundances obtained through high-throughput\
                sequencing, working towards developing a model that identifies healthy and unhealthy environments based on microbial\
                composition.\
                ■ Conducted feature importance analysis to identify the ten most important microbe ASVs that could be used to create low-cost\
                assays for the classification, resulting in perfect classification of the samples without doing high-throughput sequencing for all\
                test cases.\
                Financial Research Analyst - University of San Francisco May 2018 - May 2020\
                ■ Developed machine learning models that automatically create an investment portfolio based on stock mispricing using\
                historical financial data, achieving risk-adjusted returns of up to 10% per year when the strategy is applied on historical data.\
                High School Science Teacher - Piedmont High School 2018-2019\
                ■ During a colleague’s maternity leave, assumed a temporary teaching position, demonstrating a deep passion for education and a\
                strong commitment to inspiring and supporting students to achieve their academic success and personal goals.\
                Graduate Research Assistant – University of Maryland May 2017-August 2017\
                ■ Research position in a quantum optics laboratory developing quantum memory to be used in the repeater scheme that is\
                essential to the development of long distance quantum communication and quantum networks.\
                Research Scientist – Saratoga Energy Research Partners January 2013 – September 2013\
                ■ Development of novel anode materials for Lithium ion batteries via a stochastic deposition process of carbon during electrolysis.\
                Skills\
                ● Strong technical skills: Python, SQL, Pytorch, Keras, Tensorflow, Javascript, Flask, React, Vue, AWS, EMR, Databricks,\
                Spark, pyspark, Hadoop, React, Java, R, Dash, Tableau, Matlab, mathematical modeling, statistics"
                
cfg=config.Config()
# Set org ID and API key
openai.organization = "org-DVSnWLza0jZx39jd8LySmnUY"
openai.api_key = cfg.openai_api_key

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
    
def generate_prompt(resume):
    prompt_text = f"My Resume:  {resume} \
                   \n Please craft me a respectable, professional cover letter. It should be specific to the job and specific company information that I'm including.\
                   Also, incorporate the information from my resume that is attached to create a compelling narrative for why I would be a great fit at the company. \
                       Focus on specific items and accmoplishments on my resume.\
                    Keep it short and light but profesional. Bullets are fine if they make readability cleaner. With my resume,have it generate specific cover letter for that specific company that is about one half page.\
                    \nJob Posting: {input}"
    return prompt_text


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": generate_prompt(prompt)})

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
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
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

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
            
            
            
