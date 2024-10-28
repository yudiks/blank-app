import streamlit as st
import google.generativeai as genai
import os
import time

# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎈 Story Writer")
st.header(" Generating an inspiring story every day ")
story_title = st.text_input(label='what story you want to create?')

def stream_data(response):
    for chunk in response:
        yield chunk.text + " "
        time.sleep(2)

if len(story_title) > 0:
    response = model.generate_content(story_title, stream=True)
    st.write_stream(stream_data(response))

