import streamlit as st
import google.generativeai as genai
import pathlib
import tqdm
import os
import requests
from streamlit_pdf_viewer import pdf_viewer

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)


def download_file(url, filename):
    """Downloads a file from a URL and saves it to a file."""

    response = requests.get(url, allow_redirects=True)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def save_to_file(text, filename):
    """Downloads a file from a URL and saves it to a file."""
    with open(filename, 'wb') as file:
        file.write(text)
        print(f"File downloaded successfully: {filename}")

def summarize(file_ref):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    count_token = model.count_tokens([file_ref, '\n\nCan you summarize this file as a bulleted list? in 100 words'])

    response = model.generate_content(
        [file_ref, '\n\nCan you summarize this file as a bulleted list?']
    )
    st.text(count_token)
    st.markdown(response.text)


st.title("🎈 PDF Summarizer")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
url = st.text_input(label='enter a url')
summarize_button = st.button('Summarize')


if url == None:
    url = "https://storage.googleapis.com/generativeai-downloads/data/Smoothly%20editing%20material%20properties%20of%20objects%20with%20text-to-image%20models%20and%20synthetic%20data.pdf"
    filename = "test.pdf"
    if not os.path.exists(filename):
        download_file(url, filename)
    pdf_viewer(filename)
    file_ref = genai.upload_file(filename)
    summarize(file_ref)

if uploaded_file:
    filename = "test.pdf"
    binary_data = uploaded_file.getvalue()
    pdf_viewer(input=binary_data,
                width=700)
    save_to_file(binary_data, filename)
    file_ref = genai.upload_file(filename)
    summarize(file_ref)