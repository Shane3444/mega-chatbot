from chatbot.utils import setup_rag_chain
import streamlit as st

st.title("Travel Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

rag_chain = setup_rag_chain()

if prompt := st.chat_input("Ask anything!"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    response = rag_chain.invoke({'input': prompt})
    
    with st.chat_message("assistant"):
        st.markdown(response['answer'])
        st.session_state.messages.append({"role" : "assistant", "content" : response['answer']})