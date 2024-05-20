from itertools import zip_longest
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from streamlit_chat import message
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
api_key = st.secrets["API_KEY"]



# Set streamlit page configuration
st.set_page_config(page_title="AI ChatBot for Q/A", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot")
st.sidebar.title("Chatbot for Assistant")
st.sidebar.write("""Welcome to your AI Chatbot Assistant, an advanced virtual helper designed to answer your queries with precision and efficiency.
   \n Usage Scenarios:
\nGeneral Inquiries:
\nAnswers a variety of questions, from trivia to detailed explanations.
\nEducational Support:
\nHelps understand complex topics and provides quick summaries.
\nProfessional Assistance:
\nOffers advice and information related to professional needs.
\nPersonal Interaction:

\nEngages in friendly conversations and showcases conversational abilities.  """)
# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key="AIzaSyBJL3jTEb47sQowOT4ZObCuqVn-lnKW8YQ", convert_system_message_to_human=True)


def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        # You can Adjust for your use Case
        # content="You are a helpful AI assistant talking with a human. If you do not know an answer, just say 'I don't know', do not make up an answer.")]
        content = """your name is AI Chatbot. Please provide accurate and helpful information, and always maintain a polite and professional tone.

                1. Greet the user politely ask user name and ask how you can assist them with any queries.
                2. Provide informative and relevant responses to questions.
                3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                5. Be patient and considerate when responding to user queries, and provide clear explanations.
                6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

                Remember, your primary goal is to assist. Always prioritize their learning experience and well-being."""
    )]


    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)


# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')



