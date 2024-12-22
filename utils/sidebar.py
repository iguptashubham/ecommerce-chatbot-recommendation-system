import streamlit as st

def sidebar():
    with st.sidebar:
        with st.container(border=True):
            st.markdown('### Enter ID here', unsafe_allow_html=True)
            id = st.text_input(label='enter your id here')
            st.write(f"Enter ID - {id}")
            
            st.markdown('### response')
            with st.expander('response'):
                st.json('response')
            
            