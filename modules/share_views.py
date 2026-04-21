import streamlit as st

def render(data):

    selected_share = data

    st.dataframe(data)