"""
This is the Resume work page
"""
# Import necessary modules
import re
from io import BytesIO
from typing import List
from autogpt.config.config import Config
import streamlit as st
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
from autogpt import cli
from streamlit_chat import message
import json
import os
import time
from datetime import datetime
import base64

cfg = Config()
openai_api = cfg.openai_api_key

st.title("Resume Review")
st.markdown("\n --- \n")
# Main Description
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
    

if 'generated_res' not in st.session_state:
    st.session_state['generated_res'] = []
if 'past' not in st.session_state:
    st.session_state['past_res'] = []   
if "user_input" not in st.session_state:
    st.session_state['user_input'] = ""
if "output" not in st.session_state:
    st.session_state['output'] = ""
if 'open_api' not in st.session_state:
    st.session_state['open_api'] = None
        
# Define a function to parse a PDF file and extract its text content
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    
@st.cache_data
def parse_pdf(file: BytesIO) -> List[str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output

def main():
    @st.cache_data
    def text_to_docs(text: str) -> List[Document]:
        """Converts a string or list of strings to a list of Documents
        with metadata."""
        if isinstance(text, str):
            # Take a single string as one page
            text = [text]
        page_docs = [Document(page_content=page) for page in text]

        # Add page numbers as metadata
        for i, doc in enumerate(page_docs):
            doc.metadata["page"] = i + 1
    # Split pages into chunks
        doc_chunks = []
        for doc in page_docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                chunk_overlap=0,
            )
            chunks = text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
                )
                # Add sources a metadata
                doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
                doc_chunks.append(doc)
        return doc_chunks

    # Define a function for the embeddings
    @st.cache_data
    def test_embed():
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api)
        # Indexing
        # Save in a Vector DB
        with st.spinner("It's indexing..."):
            index = FAISS.from_documents(pages, embeddings)
        st.success("Embeddings done.", icon="✅")
        return index


    # Allow the user to upload a PDF file
    uploaded_file = st.file_uploader("**Upload Your PDF File**", type=["pdf"])
    if "update_state" not in st.session_state:
        st.session_state.update_state = False
    if uploaded_file or st.session_state.update_state:
        st.session_state.update_state = True
        doc = parse_pdf(uploaded_file)
        pages = text_to_docs(doc)
        if pages:  
            with st.expander("Show Page Content", expanded=False):
                base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
                pdf_display = (
                    f'<embed src="data:application/pdf;base64,{base64_pdf}" '
                    'width="800" height="1000" type="application/pdf"></embed>'
                )
                st.markdown(pdf_display, unsafe_allow_html=True)
                # page_sel = st.number_input(
                #     label="Select Page", min_value=1, max_value=len(pages), step=1
                # )    
                # pages[page_sel - 1]  
            if st.session_state.open_api == None:
                openai_api = st.text_input(
                        "**Enter OpenAI API Key**",
                        type="password",
                        placeholder="sk- ",
                        help="https://platform.openai.com/account/api-keys",
                    )
                if openai_api:
                    cfg.set_openai_api_key(openai_api)
                    st.write("**OpenAPI stored**")
                    st.session_state.open_api = openai_api
                    # Test the embeddings and save the index in a vector database
                    index = test_embed()
                    # Set up the question-answering system
                    qa = RetrievalQA.from_chain_type(
                        llm=OpenAI(openai_api_key=openai_api),
                        chain_type = "stuff",
                        retriever=index.as_retriever()
                    )
                    with st.spinner(
                            "Analyzing your resume: `{}` ".format("Analyzing")
                        ):
                        out = qa.run("What is this document about? What are the key points? Why is it so amazing?")
                        if out:
                            message(out)
                            llm = OpenAI(
                                    temperature=0.7, openai_api_key=openai_api, model_name="gpt-3.5-turbo"
                                )
                            memory = ConversationBufferMemory(memory_key="chat_history")
                            tools = [    
                                Tool(
                                    name="Document Query",
                                    func=qa.run,
                                    description="Useful when answering questions about document or answering questions related to the Curriculum Vitae.",
                                )
                            ]
                            prefix = """Welcome to the Document QA retrieval feedback chatbot. A work history document will be submitted for review and questions. 
                                    You have access to a single tool:"""
                            suffix = """Begin!"
                            {chat_history}
                            Question: {input}
                            {agent_scratchpad}"""

                            prompt = ZeroShotAgent.create_prompt(
                                tools,
                                prefix=prefix,
                                suffix=suffix,
                                input_variables=["input", "chat_history", "agent_scratchpad"],
                                )
                            if "memory" not in st.session_state:
                                st.session_state.memory = ConversationBufferMemory(
                                    memory_key="chat_history", return_messages=True
                                )

                            llm_chain = LLMChain(
                                llm=OpenAI(
                                    temperature=0.7, openai_api_key=openai_api, model_name="gpt-3.5-turbo"
                                ),
                                prompt=prompt,
                                )
                            agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True, return_intermediate_steps=True)
                            agent_chain = AgentExecutor.from_agent_and_tools(
                                agent=agent, tools=tools, verbose=True, memory=st.session_state.memory
                                )
                            container = st.container()
                            with container:
                                with st.form(key='my_form', clear_on_submit=True):
                                    resume_query = st.text_input(
                                        "**Insert Text Here**",
                                        placeholder="You can ask me more questions about your work history here",
                                        )
                                    submit_button = st.form_submit_button(label='Send')
                                if submit_button and resume_query:
                                    st.session_state['user_input'] = resume_query
                                    with st.spinner(
                                        "Generating Answer to your Query : `{}` ".format(resume_query)
                                        ):
                                        res = agent_chain.run(resume_query)
                                        st.session_state.generated_res.append(res)
                                        st.info(res, icon="🤖")
                                    st.session_state['past'].append(resume_query)
                                    # Allow the user to view the conversation history and other information stored in the agent's memory
                                    if st.session_state['generated_res']:
                                        st.write("Chat History")
                                        for i in range(len(st.session_state['generated_res'])-1, 0, -1):
                                            message(st.session_state["generated_res"][i], key=str(i))
                                            message(st.session_state['past_res'][i], is_user=True, key=str(i) + '_user')
                                                    

                                # Allow the user to view the conversation history and other information stored in the agent's memory
                                with st.expander("History/Memory"):
                                    st.session_state.memory

if __name__ == "__main__":
    main()