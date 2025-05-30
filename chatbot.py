# simple_chatbot_enhanced.py
import streamlit as st
import time
import datetime

# --- Custom CSS for Animated Dark Background and Styling ---
def local_css():
    css = """
    <style>
    @keyframes gradientBackground {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    body {
        /* fallback for old browsers */
        background: #1e1e2f;
        /* Chrome 10-25, Safari 5.1-6 */
        background: -webkit-linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #3a506b);
        /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #3a506b);
        background-size: 400% 400%;
        animation: gradientBackground 20s ease infinite;
        color: #E0E0E0; /* Default text color for better readability */
    }

    /* Ensure Streamlit's main content area allows background to show */
    .main .block-container {
        background-color: transparent !important;
        padding-top: 2rem; /* Adjust padding if needed */
    }

    /* Style chat messages for better readability */
    div[data-testid="stChatMessage"] > div { /* Target inner div for background */
        background-color: rgba(0, 0, 20, 0.6); /* Semi-transparent dark blueish background */
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(200, 200, 255, 0.2);
    }
    
    div[data-testid="stChatMessage"] p { /* Ensure text inside message is light */
        color: #F0F0F5;
    }

    /* Style user messages slightly differently */
    div[data-testid="stChatMessage"][data-testid="stChatMessageUser"] > div {
        background-color: rgba(20, 0, 40, 0.65); /* Slightly different shade for user */
    }

    /* Chat input area styling */
    div[data-testid="stChatInput"] {
         background-color: rgba(10, 10, 25, 0.7); /* Darker, semi-transparent */
         border-top: 1px solid rgba(200, 200, 255, 0.2);
    }
    
    /* Ensure title and caption are clearly visible */
    h1, .stCaption {
        color: #FFFFFF !important; /* Force white for title and caption */
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5); /* Subtle shadow for depth */
    }

    /* Button styling */
    .stButton>button {
        background-color: #4A4A70;
        color: white;
        border-radius: 8px;
        border: 1px solid #6A6A90;
    }
    .stButton>button:hover {
        background-color: #6A6A90;
        border: 1px solid #8A8AB0;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.75em;
        color: #A0A0B0; /* Lighter grey for timestamp */
        text-align: right;
        margin-top: 5px;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Helper Functions ---
def get_time_of_day_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# --- Bot Logic ---
def get_simple_response(user_input, session_state):
    user_input_lower = user_input.lower()
    response = ""
    user_name = session_state.get("user_name", "")

    # Greeting based on time for specific phrases
    greeting_time = get_time_of_day_greeting()
    name_to_greet = f" {user_name}" if user_name else ""

    if "hello" in user_input_lower or "hi" in user_input_lower or "hey" in user_input_lower:
        response = f"{greeting_time}{name_to_greet}! How can I help you today?"
    elif "my name is" in user_input_lower:
        try:
            name = user_input.split("my name is", 1)[1].strip().split(" ")[0] # Get the first word after "is"
            if name:
                session_state.user_name = name.capitalize()
                response = f"Nice to meet you, {session_state.user_name}! I'll try to remember that."
            else:
                response = "I didn't quite catch your name. Can you try again like 'my name is Alex'?"
        except IndexError:
            response = "I think you tried to tell me your name, but I missed it. Please say 'my name is [Your Name]'."
    elif "what is my name" in user_input_lower or "do you know my name" in user_input_lower:
        if user_name:
            response = f"I believe your name is {user_name}."
        else:
            response = "I don't think I know your name yet. You can tell me by saying 'my name is [Your Name]'."
    elif "how are you" in user_input_lower:
        response = f"I'm doing well, thank you for asking! I'm a simple bot here to assist you."
    elif "your name" in user_input_lower or "who are you" in user_input_lower:
        response = "I am a friendly Streamlit Chatbot, enhanced with a few new tricks!"
    elif "what can you do" in user_input_lower or "help" in user_input_lower:
        response = (
            "I can do a few things:\n"
            "- Greet you based on the time of day.\n"
            "- Remember your name if you tell me (e.g., 'my name is Bard').\n"
            "- Tell you the current time.\n"
            "- Tell you a simple joke.\n"
            "- Answer some basic questions.\n"
            "Try asking 'what is my name?', 'time?', or 'tell me a joke'."
        )
    elif "bye" in user_input_lower or "goodbye" in user_input_lower:
        response = f"Goodbye{name_to_greet}! Have a great day!"
    elif "time" in user_input_lower or "what's the time" in user_input_lower:
        current_time = datetime.datetime.now().strftime('%I:%M %p') # e.g., 03:45 PM
        response = f"The current time is {current_time}."
    elif "tell me a joke" in user_input_lower or "joke" in user_input_lower:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't programmers like nature? It has too many bugs.",
            "What do you call fake spaghetti? An Impasta!"
        ]
        import random
        response = random.choice(jokes)
    else:
        response = "I'm sorry, I don't quite understand that. I'm still learning! You can type 'help' to see what I can do."
    
    return response

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="Animated Chatbot") # Use wide layout

# Apply custom CSS
local_css()

st.title("🤖 Enhanced Animated Chatbot")
st.caption("A simple bot with a snazzy look and a few more features!")

# Initialize chat history and user name in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial assistant message with time-based greeting
    greeting = get_time_of_day_greeting()
    st.session_state.messages.append(
        {"role": "assistant", "content": f"{greeting}! I'm your friendly chatbot. Ask me something or type 'help'!", "timestamp": datetime.datetime.now()}
    )
if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("timestamp"):
            st.markdown(f"<div class='timestamp'>{message['timestamp'].strftime('%I:%M %p')}</div>", unsafe_allow_html=True)


# Accept user input
if prompt := st.chat_input("What is up?"):
    current_time = datetime.datetime.now()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": current_time})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        st.markdown(f"<div class='timestamp'>{current_time.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response_text = get_simple_response(prompt, st.session_state)
        # Simulate typing
        message_placeholder = st.empty()
        full_response_streamed = ""
        for chunk in response_text.split(): # Simple chunking by word
            full_response_streamed += chunk + " "
            time.sleep(0.05) # Small delay for typing effect
            message_placeholder.markdown(full_response_streamed + "▌")
        message_placeholder.markdown(full_response_streamed)
        
        # Add timestamp for assistant's full response
        assistant_time = datetime.datetime.now()
        st.markdown(f"<div class='timestamp'>{assistant_time.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)


    # Add assistant response to chat history (full response, not streamed)
    st.session_state.messages.append({"role": "assistant", "content": response_text, "timestamp": assistant_time})

# Optional: Add a button to clear chat in the sidebar for less clutter
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat History"):
        greeting = get_time_of_day_greeting()
        st.session_state.messages = [
            {"role": "assistant", "content": f"{greeting}! Chat cleared. Ask me something new!", "timestamp": datetime.datetime.now()}
        ]
        st.session_state.user_name = "" # Also clear the remembered name
        st.rerun()