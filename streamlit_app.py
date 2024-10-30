import streamlit as st
import google.generativeai as genai
import os
import time
import base64
import streamlit as st
from gtts import gTTS
from io import BytesIO

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎈 Story Writer")
st.header(" Generating an inspiring story every day ")
story_title = st.text_input('')
generate_button = st.button('Generate')

prompt = 'Create a story for 8 years old with approximately about a 400 words long about'

def stream_data(response):
    for chunk in response:
        yield chunk.text + " "
        time.sleep(1)

if generate_button and len(story_title) > 0:
    response = model.generate_content(prompt + story_title, stream=True)
    st.write_stream(stream_data(response))

    final_text = ''
    for chunk in response:
        final_text += chunk.text
    # final_text += stream_data(response)
    
    tts = gTTS(final_text, lang='en')
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    st.audio(audio_stream)