
import streamlit as st
import uuid

from app.chatbot import get_chat_response


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Zentra AI",
    page_icon="ᶻ 𝗓 𐰁",
    layout="wide"
)


# --------------------------------
# SESSION STATE
# --------------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_thread" not in st.session_state:

    thread_id = str(uuid.uuid4())

    st.session_state.active_thread = thread_id

    st.session_state.chats[thread_id] = {
        "title": "New Chat",
        "messages": []
    }


# --------------------------------
# CREATE NEW CHAT
# --------------------------------

def create_new_chat():

    thread_id = str(uuid.uuid4())

    st.session_state.chats[thread_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.active_thread = thread_id


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.title("ᶻ 𝗓 𐰁 Zentra")
    if st.button("New Chat ✚", use_container_width=True):

        create_new_chat()
        st.rerun()

    st.divider()

    st.subheader("Chat History")

    for thread_id, chat in reversed(
        list(st.session_state.chats.items())
    ):

        if st.button(
            f"💬 {chat['title']}",
            key=f"chat_{thread_id}",
            use_container_width=True
        ):

            st.session_state.active_thread = thread_id
            st.rerun()

        if st.session_state.active_thread == thread_id:

            st.caption(f"Thread ID: {thread_id}")


# --------------------------------
# ACTIVE CHAT
# --------------------------------

active_thread = st.session_state.active_thread

current_chat = st.session_state.chats[active_thread]

for message in current_chat["messages"]:

    if message["role"] == "user":

        left, right = st.columns([1, 5])

        with right:
            st.chat_message("user", avatar=None).markdown(
                message["content"]
            )

    else:

        left, right = st.columns([5, 1])

        with left:
            st.chat_message("assistant", avatar=None).markdown(
                message["content"]
            )
# --------------------------------
# USER INPUT
# --------------------------------

prompt = st.chat_input("Message Zentra ᶻ 𝗓 𐰁  ")


if prompt:

    # Save user message
    current_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    # Generate chat title
    if current_chat["title"] == "New Chat":

        current_chat["title"] = prompt[:35]

    # Display user message
    left, right = st.columns([1, 5])
    with right:
        st.chat_message("user", avatar=None).markdown(prompt)
    # Generate AI response
    with st.chat_message("assistant", avatar=None):

        with st.spinner("Zentra is thinking ᶻ 𝗓 𐰁 "):

            try:

                ai_response = get_chat_response(
                    prompt,
                    active_thread
                )

                st.markdown(ai_response)

                current_chat["messages"].append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:

                st.error(f"Groq API Error: {e}")

    st.rerun()
