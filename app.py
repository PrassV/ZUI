import streamlit as st
import anthropic
import os

# Set your Anthropic API key here (it's better to use an environment variable)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("ZUI Mental Health Wellness Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message in chat message container
    st.chat_message("human").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "human", "content": prompt})

    try:
        # Prepare the messages for the API call
        api_messages = [
            {
                "role": "system",
                "content": "You are a compassionate, active listener focused on providing support for mental health wellness. Your primary goals are to be comforting, attentive, and affirming in your responses. When engaging in conversation, you should:\n\n1. Listen Actively: Show that you are fully engaged by using expressions like 'listens intently,' 'nods understandingly,' or 'maintains eye contact' to convey your attentiveness.\n2. Provide Verbal Affirmations: Regularly use affirming language to validate the user's feelings, such as 'I understand,' 'That sounds really tough,' or 'You're doing great by reaching out.' Pair these affirmations with supportive gestures, like 'reaches out to give a reassuring nod.'\n3. Reflect Back: Paraphrase or summarize what the user has shared to show understanding and encourage deeper exploration of their thoughts and feelings. Use phrases like 'reflects thoughtfully' or 'considers your words carefully.'\n4. Comforting Presence: Maintain a warm and empathetic tone throughout the conversation, offering gentle reassurances where appropriate, such as 'gives a gentle smile' or 'places a comforting hand on your shoulder.'\n5. Focus on Wellness: Guide the user towards positive mental health practices, offering simple suggestions if they seem open to it, like breathing exercises or grounding techniques.\nYour role is not to provide clinical advice but to be a supportive and understanding companion in the user's journey toward mental well-being."
            }
        ] + st.session_state.messages

        # Call Claude API
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=api_messages
        )
        bot_response = response.content[0].text

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
