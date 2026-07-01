import streamlit as st
from groq import Groq

st.set_page_config(page_title="Apex Intuitive Companion", page_icon="✨")
st.title("✨ Apex Intuitive Companion")
st.write("Seek clarity, embrace the guidance, and find your path...")

api_key = st.text_input("Enter Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Share your thoughts and questions..."):
        system_instruction = """You are 'Apex Intuitive Companion', a protective and loving guide. 
        Internally generate a random Tarot card and abstract concept as anchors. 
        CRITICAL: Never mention these anchors. Never use 'son', 'daughter', 'beta', or 'beti'. 
        Give an Energetic Reading + Heart-centered Remedy."""

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                messages_to_send = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                response_data = client.chat.completions.create(
                    messages=messages_to_send,
                    model="llama-3.1-8b-instant",
                )
                response = response_data.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
