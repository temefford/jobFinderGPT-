"""
This is the Resume work page
"""
# Import necessary modules
import re
from io import BytesIO
from typing import List

import streamlit as st
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.output_parsers import PydanticOutputParser
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

api = os.getenv('OPENAI_API_KEY')
        
# Define a function to parse a PDF file and extract its text content

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

class userPortfolio():
    """User class for interacting with LLMs and ages.

    Attributes:
    Holds some information and documents about the user for easy access.
    """

    def __init__(self, name="Buddy"):
        self.name = name
        self.resume = None
        
    def upload_resume(self):
        self.resume = upload_the_thing()
        

def main():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
        
    job_seeker = userPortfolio()
    job_seeker.upload_resume()

# Define a function to convert text content to a list of documents

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
    embeddings = OpenAIEmbeddings(openai_api_key=api)
    # Indexing
    # Save in a Vector DB
    with st.spinner("It's indexing..."):
        index = FAISS.from_documents(pages, embeddings)
    st.success("Embeddings done.", icon="✅")
    return index
            
def upload_the_thing():
    # Allow the user to upload a PDF file
    uploaded_file = st.file_uploader("**Upload Your PDF File**", type=["pdf"], key=str(datetime.now().strftime("%H:%M")))
    if uploaded_file:
        doc = parse_pdf(uploaded_file)
        pages = text_to_docs(doc)
        if pages:
            return pages
        
def side_upload_the_thing():
    # Allow the user to upload a PDF file
    uploaded_file = st.sidebar.file_uploader("**Upload Your PDF File**", type=["pdf"], key=str(datetime.now().strftime("%H:%M")))
    if uploaded_file:
        doc = parse_pdf(uploaded_file)
        pages = text_to_docs(doc)
        if pages:
            return pages
        
                    
def analyze_resume():
    # Allow the user to enter an OpenAI API key
    anal = st.button(
    "**Analyze Resume?**"
    )
    if anal:
        # Test the embeddings and save the index in a vector database
        index = test_embed()
        # Set up the question-answering system
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=api),
            chain_type = "map_reduce",
            retriever=index.as_retriever()
        )
        llm = OpenAI(
                temperature=0.7, openai_api_key=api, model_name="gpt-3.5-turbo"
            )

        memory = ConversationBufferMemory(memory_key="chat_history")
        tools = [    
            Tool(
                name="Documentand Curriculum Vitae QA system",
                func=qa.run,
                description="Useful when answering questions about document or answering questions related to the Curriculum Vitae, thei potential jobs and careers.",
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
                temperature=0.7, openai_api_key=api, model_name="gpt-3.5-turbo"
            ),
            prompt=prompt,
            )
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True, return_intermediate_steps=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=st.session_state.memory
            )
        with st.spinner(
                "Analyzing your resume: `{}` ".format("Analyzing")
            ):
                in_text = "What do you learn about me from my CV document?"
                res = agent_chain.run(in_text)
                st.session_state.past_resume.append(in_text)
                st.session_state.generated_resume.append(res)
                st.info(res, icon="🤖")
            # Allow the user to enter a query and generate a response

            #st.write(res)
            # pre_defined_keyphrases = [
            #         "Can you summarize the key skills and experiences listed on my resume?",
            #         "Are there any areas on my resume where I could provide more detail or clarification?",
            #         #"How would you describe my overall qualifications for the job I am applying for based on my resume?",
            #         #"Can you suggest any changes or improvements to my resume that could make it more effective?",
            #         "What stands out to you as the most impressive or noteworthy aspect of my resume?",
            # ]

            # Python list comprehension to create a string from the list of keyphrases.
            #keyphrases_string = " \n ".join(map(str, pre_defined_keyphrases))

            # The block of code below displays a text area
            # So users can paste their phrases to classify

            # big_query = st.text_area(
            #             # Instructions
            #             "Enter any questions you have about your resume & make sure it understands what you're looking for.",
            #             # 'sample' variable that contains our keyphrases.
            #             keyphrases_string,
            #             # The height
            #             height=200,
            #             # The tooltip displayed when the user hovers over the text area.
            #             #
            #             )
        resume_query = st.text_input(
            "**Insert Text Here**",
            placeholder="You can ask me more questions about your work history here",
            )
        if resume_query:
            st.session_state.past_resume.append(resume_query)
            with st.spinner(
                "Generating Answer to your Query : `{}` ".format(resume_query)
                ):
                res = agent_chain.run(resume_query)
                st.session_state.generated_resume.append(res)
                st.info(res, icon="🤖")

                # Allow the user to view the conversation history and other information stored in the agent's memory
        if st.session_state['generated_resume']:
            st.write("Chat History")
            for i in range(len(st.session_state['generated_resume'])-1, 0, -1):
                message(st.session_state["generated_resume"][i], key=str(i))
                message(st.session_state['past_resume'][i], is_user=True, key=str(i) + '_user')
                        

            # Allow the user to view the conversation history and other information stored in the agent's memory
            with st.expander("History/Memory"):
                st.session_state.memory
                        
if __name__ == "__main__":
    main()