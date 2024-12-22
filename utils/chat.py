import streamlit as st
import requests

def get_response(url:str,query:str)->dict:
    input_data = {'userinput':query}
    response = requests.post(url=url,json=input_data)
    if response.status_code==200:
        result = response.json()
        return result
    else:
        print('unable to get response from url')

def chatbot():
    chat_input = st.text_input('Enter your message here')
    with st.chat_message('human'):
        st.write(chat_input)
    answer = get_response(url='http://127.0.0.1:600/chat',query=chat_input)
    with st.chat_message('ai'):
        st.write(answer['response']['answer'])