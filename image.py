
import google.generativeai as genai
import PIL.Image
# from IPython.display import display, Image, HTML
# import ipywidgets as widgets
import json
from typing_extensions import TypedDict
from PIL import Image
import requests
from io import BytesIO
import os
import streamlit as st

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name='gemini-1.5-flash')

productSketchUrl = "https://storage.googleapis.com/generativeai-downloads/images/jetpack.jpg"
response = requests.get(productSketchUrl)
img = Image.open(BytesIO(response.content))


# img = PIL.Image.open(img_from_url)
# display(Image('jetpack.jpg', width=300))

analyzePrompt = """This image contains a sketch of a potential product along with some notes.
Given the product sketch, describe the product as thoroughly as possible based on what you
see in the image, making sure to note all of the product features.

Return output in json format."""



class Response(TypedDict):
  description: str
  features: list[str]


response = model.generate_content(
    [analyzePrompt, img],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=Response))

productInfo = json.loads(response.text)
print(json.dumps(productInfo, indent=4))

st.write(response.text)
