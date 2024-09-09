import streamlit as st
from streamlit_pills import pills

st.title("Preferences")

if "config" not in st.session_state:
    st.session_state.config = False

def submit():
    if st.button("Submit"):
        st.session_state.config = True
        st.switch_page(st.Page("chatbot/bot.py"))

#Initializing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

group_option = None
duration_option = pills("Duration", options=["5 nights 6 days", "9 nights 10 days", "Other"])
month_option = pills("Month of Arrival", options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
ig_option = pills("Individual / Group", options=["Individual", "Group"])
if ig_option == "Group":
    group_option = pills("Type of Group", options=["FIT", "Student", "Leisure", "Incentive"])
user_pref = {
    "Duration" : duration_option,
    "Month" : month_option,
    "Group" : ig_option,
    "Type" : group_option if group_option else None
}
st.session_state["preferences"] = user_pref
submit()

# with st.chat_message("assistant"):
#         st.markdown(f"{duration_option}, {month_option}, {ig_option}, {group_option}")

# if prompt := st.chat_input("What's up?"):
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role" : "user", "content" : prompt})
#     response = prompt

#     with st.chat_message("assistant"):
#         st.markdown(response)

#     st.session_state.messages.append({"role" : "assistant", "content" : response})