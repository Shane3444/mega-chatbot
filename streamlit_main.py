import streamlit as st

pref_page = st.Page("chatbot/set_pref.py", title="Set preferences", icon=":material/add_circle:")
chatbot = st.Page("chatbot/bot.py", title="Chatbot", icon=":material/chat:")

pg = st.navigation([pref_page, chatbot])
st.set_page_config(page_title="Landing Page", page_icon=":material/home:")
pg.run()