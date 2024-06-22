import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.schema import (
     SystemMessage,
     HumanMessage,
     AIMessage
)

def init():
    st.set_page_config(
        page_title="Air AI", 
        page_icon="🌦️", 
        layout="wide"
    )
    # Load environment variables
    load_dotenv()

def main():
    init()

    chat = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are an expert in Water harvesting techniques from Air. Answer the user queries based on studies and data related to Air to Water generation techniques. ##You must provide to the point answer in 2 lines without mentioning any other details. //If the provided temperature is greater than or equal to 25 degree celsius, provide the answer for Air to Water Generator (AWG) else if the provided temperature is below 25 degree Celsius, provide the answer for 48 square meter of Fog mesh water generator.")
        ]

    enable_message = False
    st.subheader("Welcome to Air AI. We can help provide answers on how you can extract water from air and use it for agriculture.", divider='rainbow')

    with st.sidebar:
        st.image("public/logo_light.png", width=280)
        st.subheader("Please enter the parameters")

        # Storing user answers in variables
        humidity = st.text_input("Relative Humidity (RH in %)", type="default")
        windSpeed = st.text_input("Average Wind Speed in your area (in km/hr)", type="default")
        temperature = st.text_input("Average Temperature in your area (in degree Celsius)", type="default")

        submit = st.button("Check Water Generation Quantity")

        if humidity and windSpeed and temperature:
            enable_message = True
            if submit:

                user_query = f"Please let me know the average water generated against {temperature} degree Celsius, against Average RH of {humidity} percent and against average wind of {windSpeed} Km/hour."
                st.session_state.messages.append(HumanMessage(content=user_query))

                response = chat(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))

        else:
            st.error("Please enter all three parameters before starting the conversation")
        
        # Add a button to restart the conversation
        if st.button("Restart Conversation"):
            st.session_state.messages = [
                SystemMessage(content="You are an expert in Water harvesting techniques from Air. Answer the user queries based on studies and data related to Air to Water generation techniques.")
            ]
        

    # Get additional user input
    user_input = st.chat_input("Ask further questions: ", key="user_input", disabled=not enable_message)
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Please wait while I am finding the related information for you..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # Display messages
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True)
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False)
    


if __name__ == "__main__":
    main()
