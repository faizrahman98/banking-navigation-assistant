import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_option_menu import option_menu
from util import record_audio,generate_answer,transcribe_audio,text_speech,save_audio
import elevenlabs
import os
from st_audiorec import st_audiorec  # Import the audio recorder component
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment

# Define the names for the user and the bot
USER_NAME = "John"
BOT_NAME = "MegaloBot"
LOGO_IMAGE = 'logo.webp'

# Parameters for recording
duration = 5  # seconds
fs = 44100  # Sample rate
channels = 1  # Mono recording

# Border width variables
border_width_metric1 = 0  # For first metric card
border_width_metric2 = 0  # For second metric card
border_width_graph1 = 0   # For first graph
border_width_graph2 = 0   # For second graph
border_width_table = 0    # For the dataframe table

def reset_highlight():
    # Border width variables
    border_width_metric1 = 0  # For first metric card
    border_width_metric2 = 0  # For second metric card
    border_width_graph1 = 0   # For first graph
    border_width_graph2 = 0   # For second graph
    border_width_table = 0
  
# Custom CSS to hide the tooltip
hide_streamlit_style = """
            <style>
        .st-emotion-cache-1y4p8pa{
            padding: 2rem 1rem 10rem!important;
        }
            .menu .nav-item .nav-link.active[data-v-5af006b8] {
    background-color: #2430ae!important;
}
           .stChatMessage{
    border: 1px solid #cccccc!important;
}
        
        .st-emotion-cache-1xarl3l.e1i5pmia1{
            box-shadow: 0 0 4px black!important;
    background: #2430ae!important;
    color: white!important;
    margin-right: 0.8rem;
        }
         .element-container.st-emotion-cache-1q2b4v7.e1f1d6gn4 label{
          
    color: white!important;
        }
            </style>
            """

# Dummy data for recent transactions
df_transactions = pd.DataFrame({
    'Transaction': ['Groceries', 'Utilities', 'Rent', 'Gym', 'Coffee'],
    'Amount': [120.50, 60.75, 1500.00, 45.00, 4.25],
    'Date': pd.to_datetime(['2024-02-20', '2024-02-18', '2024-02-01', '2024-02-15', '2024-02-22']),
    'Category': ['Food', 'Bills', 'Housing', 'Health', 'Food']
})

# Dummy data for credit analysis
df_credit = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=6, freq='ME'),
    'Credit Score': np.random.randint(600, 800, 6)
})

# Dummy data for spending analysis
df_spending = pd.DataFrame({
    'Category': ['Food', 'Shopping', 'Bills', 'Travel', 'Entertainment', 'Health'],
    'Amount': np.random.randint(100, 500, 6),
    'Date': pd.date_range(start='2024-02-01', periods=6, freq='ME')
})
# Inject custom CSS with markdown
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Function placeholder for processing audio input
def process_audio_input(audio_data):
    # Placeholder function to process audio input
    # Here you would add your audio processing code
    st.write("Audio data received...")

# Function placeholder for generating audio output
def generate_audio_output():
    # Placeholder function to generate audio output
    st.write("Generating audio output...")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []




# Create the sidebar with navigation
with st.sidebar:
    st.sidebar.title('AI Assistant')
    app_mode = "Home"
    
        # Chatbot area
    with st.container():
        # st.write("Chat with :blue[**VelocitrApp**]")
        st.markdown(f'<p style="color: #0d6efd;font-size: 1rem;text-align:center;font-weight: 600;box-shadow: inset 0 0 1px 1px #d8e1ff;border-radius: 5%; padding: 0.4rem;">Chat with VelocitorApp</p>', unsafe_allow_html=True)
        # New chat UI
        messages_container = st.container(height=350,border=None)
        col1, col2 = st.columns([5, 1])
        with col1: 
            prompt = st.chat_input("Say something")
        with col2:
            audio_bytes = audio_recorder(sample_rate=44100,text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_size="2x")
        if prompt:
            st.session_state["messages"].append(("user", prompt))
            response = generate_answer(prompt)  # Assuming generate_answer is defined
            if ']' in response:
                [str_num,response] = response.split(']')
                num = int(str_num[1])
                border_width_metric1 = 0  # For first metric card
                border_width_metric2 = 0  # For second metric card
                border_width_graph1 = 0   # For first graph
                border_width_graph2 = 0   # For second graph
                border_width_table = 0
                if num == 0:
                     pass
                elif num == 1:
                    border_width_metric1 = 2
                elif num ==2:
                    border_width_metric2 = 2
                elif num == 3:
                    border_width_graph1 = 2
                elif num == 4:
                    border_width_graph2 = 2
                elif num == 5:
                    border_width_table = 2
                
            st.session_state["messages"].append(("bot", response))
        # Record audio button
        
        # Audio transcription and response
        if audio_bytes is not None:
            audio_file = "audio.wav"
            with open(audio_file, "wb") as f:
                f.write(audio_bytes)
    
            # Load the stereo audio and convert to mono
            stereo_audio = AudioSegment.from_file(audio_file, format="wav")
            mono_audio = stereo_audio.set_channels(1)
            os.remove(audio_file)
            maudio_file = "audio1.wav"
            mono_audio.export(maudio_file, format="wav")
    
            transcription = transcribe_audio(maudio_file)
            st.session_state["messages"].append(("user", transcription))
    
            # Generate and display response
            answer = generate_answer(transcription)
            if ']' in answer:
                [str_num,response] = answer.split(']')
                num = int(str_num[1])
                border_width_metric1 = 0  # For first metric card
                border_width_metric2 = 0  # For second metric card
                border_width_graph1 = 0   # For first graph
                border_width_graph2 = 0   # For second graph
                border_width_table = 0
                if num == 0:
                     pass
                elif num == 1:
                    border_width_metric1 = 2
                elif num ==2:
                    border_width_metric2 = 2
                elif num == 3:
                    border_width_graph1 = 2
                elif num == 4:
                    border_width_graph2 = 2
                elif num == 5:
                    border_width_table = 2
                st.session_state["messages"].append(("bot", response))
            audioout = text_speech(response)
            elevenlabs.play(audioout)
            os.remove(maudio_file)
            
            
        # Display chat messages
        for role, message in st.session_state["messages"]:
            if role == "user":
                messages_container.chat_message("user").write(f"{message}")
            elif role == "bot":
                messages_container.chat_message("assistant").write(f"{message}")

if app_mode == "Home":
    col1,col2 = st.columns([1,9])
    with col1:
        st.image(LOGO_IMAGE, width=80)
    with col2:
        st.title("Bank-o-saurus")
        # Balance Overview Card
    
    # Example data for charts (you'll replace this with your actual data)
    df_transactions = pd.DataFrame({
        'Transaction': ['Groceries', 'Utilities', 'Rent'],
        'Amount': [150, 75, 1200],
        'Date': pd.date_range('2023-01-01', periods=3)
    })

    df_credit = pd.DataFrame({
        'Date': pd.date_range('2023-01-01', periods=10),
        'Credit Score': np.random.randint(600, 800, 10)
    })

    df_spending = pd.DataFrame({
        'Category': ['Food', 'Shopping', 'Bills', 'Travel'],
        'Amount': np.random.randint(100, 500, 4)
    })
    balance, monthly_expenses = 45000, 4000
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
    <div style="border: {border_width_metric1}px solid red;">
    """, unsafe_allow_html=True)
        st.metric("Balance", f"${balance:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="border: {border_width_metric2}px solid blue;">    """, unsafe_allow_html=True)
        st.metric("Avg Monthly Expenses", f"${monthly_expenses:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Spending Analysis Chart - Assuming you have a dataframe `df_spending`
        st.markdown(f"""
        <div style="border: {border_width_graph1}px solid red;">
        """, unsafe_allow_html=True)
        st.subheader("Spending Analysis")
        spending_chart = alt.Chart(df_spending).mark_bar().encode(
            x='Category',
            y='Amount'
        )
        st.altair_chart(spending_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="border: {border_width_graph2}px solid red;">
        """, unsafe_allow_html=True)
        # Credit Analysis Chart - Assuming you have a dataframe `df_credit`
        st.subheader("Credit Analysis")
        credit_chart = alt.Chart(df_credit).mark_line().encode(
            x='Date',
            y='Credit Score'
        )
        st.altair_chart(credit_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Transactions - Assuming you have a dataframe `df_transactions`
    st.markdown(f"""
        <div style="border: {border_width_table}px solid red;">
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.subheader("Recent Transactions")
    st.dataframe(df_transactions)  # Display the dataframe as a table

   


    
    
            # # Audio recorder component
            # wav_audio_data = st_audiorec()
    
            # if wav_audio_data is not None:
            #     # Process the audio data
            #     process_audio_input(wav_audio_data)
            #     # Display the audio player with the recorded audio
            #     st.audio(wav_audio_data, format='audio/wav')

elif app_mode == "About":
    st.title('About')
    st.write('Information about the application and its functionalities.')