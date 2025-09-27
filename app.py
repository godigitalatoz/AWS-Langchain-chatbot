import streamlit as st
from dotenv import load_dotenv
import os
from langchain_aws import ChatBedrock

# Load AWS credintials from .env
load_dotenv()

# Initialize chat model
chat = ChatBedrock(
    model_id="amazon.titan-text-lite-v1",   # or Claude if you prefer
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2")
)

# Streamlit setup
st.set_page_config(page_title="AWS Bedrock Chatbot", layout="wide", initial_sidebar_state="expanded")
st.title("AWS Bedrock Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Model response
    response = chat.invoke(prompt)
    answer = response.content

    # Add assistant message
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state["message"] = []
        st.experimental_rerun()
        
