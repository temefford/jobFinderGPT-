# Import necessary modules
import re
from io import BytesIO
from typing import List

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
from streamlit_chat import message
import json
import os

api = os.getenv('OPENAI_API_KEY')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
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

def main():
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

    #def main():
        
    # Allow the user to upload a PDF file
    uploaded_file = st.file_uploader("**Upload Your PDF File**", type=["pdf"])
    if "update_state" not in st.session_state:
        st.session_state.update_state = False
    if uploaded_file or st.session_state.update_state:
        st.session_state.update_state = True
        name_of_file = uploaded_file.name
        doc = parse_pdf(uploaded_file)
        pages = text_to_docs(doc)
        if pages:
            # Allow the user to select a page and view its content
            with st.expander("Show Page Content", expanded=False):
                page_sel = st.number_input(
                    label="Select Page", min_value=1, max_value=len(pages), step=1
                )
                pages[page_sel - 1]
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
                        name="Document summary QA system",
                        func=qa.run,
                        description="Useful when anaswering questions about document or looking at documents to summarize and give suggestions.",
                    )
                ]
                prefix = """Have a conversation with a human, answering the following questions as best you can based on the context and memory available. 
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
                        in_text = "What do you learn about me from my resume? What type of job should I look for? How should I improve my resume? What is the strongest aspect of my resume? Do you have any suggestions for me to help me get a job?"
                        res = agent_chain.run(in_text)
                        st.session_state.past.append(in_text)
                        st.session_state.generated.append(res)
                        st.info(res, icon="🤖")
                # Allow the user to enter a query and generate a response
                
                #st.write(res)
                query = st.text_input(
                    "**Insert Text Here**",
                    placeholder="Ask me more questions here {}".format(name_of_file),
                )
                st.session_state.past.append(query)

                if query:
                    with st.spinner(
                        "Generating Answer to your Query : `{}` ".format(query)
                    ):
                        res = agent_chain.run(query)
                        st.session_state.generated.append(res)
                        st.info(res, icon="🤖")
                
            if st.session_state['generated']:
                st.write("Chat History")
                for i in range(len(st.session_state['generated'])-1, 0, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                            

                # Allow the user to view the conversation history and other information stored in the agent's memory
                with st.expander("History/Memory"):
                    st.session_state.memory
                    
if __name__ == "__main__":
    main()