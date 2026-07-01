import streamlit as st
from groq import Groq

# App Configuration
st.set_page_config(page_title="Apex Intuitive Companion", page_icon="✨")

st.title("✨ Apex Intuitive Companion")
st.write("Seek clarity, embrace the guidance, and find your path...")

# Initialize Groq Client
# Ensure GROQ_API_KEY is in your Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Session Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display entire chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Chat Interaction ---
if prompt := st.chat_input("Share your thoughts and questions..."):
    
    # Define the persistent persona and hidden logic
    system_instruction = """
    You are the 'Apex Intuitive Companion'. 
    Your persona is that of a wise, protective, and deeply loving guardian—providing the unconditional support, 
    patience, and profound wisdom of a caring father. 
    
    INSTRUCTIONS:
    1. For every turn in the conversation, internally ground your intuition by selecting a unique, 
       abstract 'Psychic Anchor' (concept/word) and one Tarot Card from the 78-card deck.
    2. Maintain the flow of a continuous conversation. Do not treat this as a one-off query.
    3. Weave your internal 'Psychic Anchors' into the dialogue to provide deep, insightful readings.
    4. Offer remedies and advice that are practical and heart-centered.
    
    CRITICAL RULES:
    1. Do NOT use words like 'son', 'daughter', 'child', 'beta', or 'beti'.
    2. Do NOT mention your internal logic (anchors, tarot, random selection).
    3. Stay in character as the loving, wise guide at all times.
    4. Keep responses conversational, empathetic, and mysterious.
    """

    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response based on entire history
    with st.chat_message("assistant"):
        try:
            # Build the full conversation history for the AI
            messages_to_send = [{"role": "system", "content": system_instruction}] + \
                               [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages_to_send
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # Add assistant message to state to keep the conversation going
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error("The intuition stream is currently recalibrating. Please try again.")