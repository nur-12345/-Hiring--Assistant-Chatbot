import streamlit as st
from conversation_manager import ConversationManager
from config import EXIT_KEYWORDS

st.set_page_config(page_title="TalentScout Hiring Assistant")

st.title("🤖 TalentScout Hiring Assistant")

# Initialize session
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ConversationManager()
    st.session_state.messages = []

    # Auto greeting
    greeting = st.session_state.chat_manager.handle_message("")
    st.session_state.messages.append(("assistant", greeting))


# Display previous messages
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)


user_input = st.chat_input("Type your message here...")

if user_input:

    if user_input.lower() in EXIT_KEYWORDS:
        st.chat_message("assistant").write(
            "Conversation ended. Thank you for applying to TalentScout!"
        )
        st.stop()

    response = st.session_state.chat_manager.handle_message(user_input)

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("assistant", response))

    with st.chat_message("assistant"):
        st.write(response)
