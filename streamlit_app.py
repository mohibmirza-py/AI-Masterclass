from groq import Groq
import streamlit as st


api_key = st.secrets['GROQ_API_KEY']
client = Groq(api_key=api_key)

def get_completion(system_prompt, conversation_history):

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + conversation_history,
    )

    return response.choices[0].message.content.strip()



def main():

    st.title("Conversational AI Bot")
    st.write("Chat with the AI. Type 'exit' to end the conversation.")


    system_prompt = "You are a helpful assistant."

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    user_input = st.chat_input("You: ")

    if user_input is not None:

        if user_input.lower() == 'exit':
            st.write("### Ending the conversation.")
            return

        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get the LLM's response
        response = get_completion(system_prompt, st.session_state.messages)
        
        # Add assistant's response to conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()
