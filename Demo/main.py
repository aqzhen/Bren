from superpowered import create_chat_thread, get_chat_response, set_api_key
from dotenv import load_dotenv
import os
import streamlit as st


load_dotenv()

# superpowered api key
set_api_key(os.getenv("SUPERPOWERED_KEY"),
            os.getenv("SUPERPOWERED_PASS"))

# set parameters
kb_id = os.getenv("KNOWLEDGEBASE_ID")
use_rse = True
segment_length = "medium"
system_message = (
    "You are a chatbot tasked with responding to questions about the PennLabs notion pages.\n\n"
    "You should never answer a question with a question, and you should always respond with the most relevant documentation page.\n\n"
    "Do not answer questions that are not about the PennLabs notion pages.\n\n"
)

# # create chat thread
# chat_thread = create_chat_thread(knowledge_base_ids=[
#                                  kb_id], use_rse=use_rse, model="gpt-3.5-turbo", segment_length=segment_length, system_message=system_message)
# chat_thread_id = chat_thread['id']
# print(f"Chat thread created with ID: {chat_thread_id}")


def generate_chatbot_response(chat_thread_id: str, user_message: str) -> str:
    """
    Generate a chatbot response using the Superpowered AI

    Args:
        user_message (str): User message

    Returns:
        str: Chatbot response
    """

    # get AI response
    print(chat_thread_id)
    chat_response = get_chat_response(chat_thread_id, user_message)
    chat_response = chat_response["interaction"]["model_response"]["content"]
    return chat_response


def handle_style_and_responses(chat_history):
    human_style = "background-color: #e6f7ff; border-radius: 10px; padding: 10px;"
    chatbot_style = "background-color: #f9f9f9; border-radius: 10px; padding: 10px;"

    for i, (role, message) in enumerate(chat_history):
        alignment = "right" if role == "User" else "left"
        style = human_style if role == "User" else chatbot_style

        st.markdown(
            f"<p style='text-align: {alignment};'><b>{role}</b></p> <p style='text-align: {
                alignment};{style}'> <i>{message}</i> </p>",
            unsafe_allow_html=True,
        )


def main():
    load_dotenv()

    if "chat_thread_id" not in st.session_state:
        st.session_state.chat_thread_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.set_page_config(
        page_title="Bren",
        page_icon=":books:",
    )

    st.title("Bren")
    st.subheader("Chat with your knowledge base!")

    user_question = st.text_input("Ask your question")

    with st.spinner("Processing..."):
        if user_question:
            if st.session_state.chat_thread_id is None:
                # Create a new chat thread for the first question
                chat_thread = create_chat_thread(knowledge_base_ids=[
                                                 kb_id], use_rse=use_rse, model="gpt-3.5-turbo", segment_length=segment_length, system_message=system_message)
                st.session_state.chat_thread_id = chat_thread['id']
                st.write(f"Chat thread created with ID: {
                         st.session_state.chat_thread_id}")

            # Get chatbot response for the current question
            chatbot_response = generate_chatbot_response(
                st.session_state.chat_thread_id, user_question)

            # Update the chat history
            st.session_state.chat_history.append(("User", user_question))
            st.session_state.chat_history.append(("Chatbot", chatbot_response))

            # Display the entire conversation
            handle_style_and_responses(st.session_state.chat_history)


if __name__ == "__main__":
    main()
