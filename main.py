import streamlit as st
from openai import OpenAI

# Set your OpenAI API key
api_key = "your API key here"

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# For light/dark mode
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

def show_messages(messages):
    chat_history = ""
    for message in messages:
        if message["role"] == "user":
            chat_history += f"""
            <div style="display: flex; justify-content: flex-end; padding: 10px; max-width: 80%;">
                <div style="background-color: #006AFF; color: #fff; padding: 10px; border-radius: 10px; max-width: calc(100% - 40px); word-wrap: break-word;">{message["content"]}</div>
            </div>
            """
        else:
            response = message["content"].replace("\n", " ")
            chat_history += f"""
            <div style="display: flex; justify-content: flex-start; padding: 10px; max-width: 80%;">
                <div style="background-color: #e6e6e6; color: #000; padding: 10px; border-radius: 10px; max-width: calc(100% - 40px); word-wrap: break-word;">{response}</div>
            </div>
            """
    return chat_history

def main():
    st.set_page_config(layout="centered", page_icon="🤖", page_title="AI Chatbot")

    st.markdown(
        """
        <style>
            .chat-box {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: auto;
                height: 70vh;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .chat-container {
                overflow-y: auto;
                flex-grow: 1;
                margin-bottom: 5px; /* Reduced gap */
            }
            .input-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 5px; /* Reduced gap */
            }
            .input-container input {
                flex-grow: 1;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
                margin-right: 10px;
            }
            .input-container button {
                background-color: #006AFF;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            body.dark-mode {
                background-color: #111;
                color: #fff;
            }
            .chat-box.dark-mode {
                background-color: #333;
            }
            .input-container input.dark-mode {
                background-color: #444;
                color: #fff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("AI Chatbot")


    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    chat_history_container = st.empty()
    chat_history_container.markdown(show_messages(st.session_state["messages"]), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    with st.form(key="chat_form"):
        user_input = st.text_input("", key="user_input", label_visibility="collapsed", placeholder="Type your message here...")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            # Add user message to chat history
            st.session_state["messages"].append({"role": "user", "content": user_input})

            # Send message to GPT-4
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=st.session_state["messages"]
                )
                assistant_message = response.choices[0].message.content
                # Add assistant response to chat history
                st.session_state["messages"].append({"role": "assistant", "content": assistant_message})

                # Update chat history with the new content
                chat_history_container.markdown(show_messages(st.session_state["messages"]), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
