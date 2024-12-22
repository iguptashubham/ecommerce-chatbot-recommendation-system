import streamlit as st 
from utils.sidebar import sidebar
from utils.chat import chatbot

st.set_page_config(page_title='MistralAI Chatbot',layout='wide')
st.title('Ecommerce Chatbot')

sidebar()
chatbot()
