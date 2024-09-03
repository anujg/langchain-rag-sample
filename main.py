from dotenv import load_dotenv

load_dotenv()
from typing import Set

import streamlit as st
from streamlit_chat import message
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import Docx2txtLoader

from backend.core import run_llm
from consts import INDEX_NAME


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

def main():
    st.header("A Simple Langchain based Chatbot with RAG Usage")
    if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
    ):
        st.session_state["chat_answers_history"] = []
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_history"] = []

    uploaded_file = st.file_uploader("Upload a PDF,Word,Text or markdown file", type=["pdf","doc","docx","txt","md"])

    if uploaded_file :
        file_name = uploaded_file.name
        temp_file = "./"+file_name
        with open(temp_file, "wb") as file:
            file.write(uploaded_file.getvalue())

        loader = None
        documents = []
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(temp_file)
            documents = loader.load_and_split()
        elif file_name.endswith(".doc") or file_name.endswith(".docx"):
            loader = Docx2txtLoader(temp_file)
            documents = loader.load()
        elif file_name.endswith(".txt") or file_name.endswith(".md"):
            loader = TextLoader(temp_file)
            documents = loader.load_and_split()
        
        # documents = loader.load_and_split()
        for doc in documents:
            new_url = doc.metadata["source"]
            new_url = file_name
            doc.metadata.update({"source": new_url})

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        print(f"Going to add {len(documents)} to Pinecone")
        PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME)
        print("****Loading to vectorstore done ***")


    prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
        "Submit"
    )

    if prompt:
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt, chat_history=st.session_state["chat_history"]
            )

            sources = set(doc.metadata["source"] for doc in generated_response["context"])

            formatted_response = (
                f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
            )

            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answers_history"].append(formatted_response)
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response["answer"]))


    if st.session_state["chat_answers_history"]:
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(
                user_query,
                is_user=True,
            )
            message(generated_response)

if __name__=="__main__":
    main()