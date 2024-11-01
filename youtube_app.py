import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎈 Youtube Summarizer")
youtube_url = st.text_input('')
summarize_button = st.button('Summarize')

video_id = "Ji2bW1aP1jo"

resp = YouTubeTranscriptApi.get_transcript(video_id, ['en'])

with open('transcript.txt', 'wb') as file:
    for i in resp:
        file.write(i['text'] + '\n')
print("File saved successfully: transcript.txt")


text_file_name = "transcript.txt"
print(f"Uploading file...")
text_file = genai.upload_file(path=text_file_name)
print(f"Completed upload: {text_file.uri}")

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
prompt = "Find ten lighthearted moments in this text file."
response = model.generate_content([prompt, text_file],
                                  request_options={"timeout": 600})
st.markdown(response.text)
