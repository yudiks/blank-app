import streamlit as st
import google.generativeai as genai
import os

# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎈 Story Writer")
story_title = st.text_input('what story you want to create?')

if len(story_title) > 0:
    response = model.generate_content(story_title, stream=True)
    for chunk in response:
        st.write(chunk.text)
