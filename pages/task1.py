import os
from pathlib import Path
from openai import AzureOpenAI
import streamlit as st
from dotenv import load_dotenv
from code_editor import code_editor
import json

st.set_page_config(page_title="Task 1", page_icon="ipt_logo.png", layout="wide")
st.markdown(Path("README_task1.md").read_text())

# load environment
load_dotenv()

# instantiate azure openai client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# add widgets
prompt_input = "Ms Holle would like to send 62 invitations for her 70th birthday. She has 17 stamps left. 11 guests live abroad, whose invitations she has to frank with one more stamp. How many more stamps does she need to buy? "

height = 20
language = "json"
wrap = True
editor_btns = [
    {
        "name": "Submit",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "alwaysOn": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    }
]

prompt_input = (
    """[
{
    "role": "system", 
    "content": "You are a helpful assistant."
},
{
    "role": "user", 
    "content": "%s"
}
]"""
    % prompt_input
)

# code editor
response_dict = code_editor(
    prompt_input, height=height, lang="json", buttons=editor_btns, options={"wrap": True}
)
output_text = st.markdown("")

# call openai
if len(response_dict["id"]) != 0 and (
    response_dict["type"] == "selection" or response_dict["type"] == "submit"
):
    # Capture the text part
    output_text.markdown("")
    response = client.chat.completions.create(
        model="gpt-35-turbo", messages=json.loads(response_dict["text"])
    )

    answer_openai = response.choices[0].message.content
    output_text.markdown(answer_openai)
