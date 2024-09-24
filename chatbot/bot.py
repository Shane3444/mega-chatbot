from utils import rag_chain
import streamlit as st

st.title("Travel Assistant")

st.session_state.counter = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything!"):
    st.chat_message("user").markdown(prompt)
    response = rag_chain(prompt, st.session_state.messages)
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    st.session_state.counter += 1
    if st.session_state.counter == 3:
        with st.chat_message("assistant"):
            st.markdown("For detailed information please contact us via email: mail@gmail.com")
            st.session_state.counter = 0
    
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role" : "assistant", "content" : response})