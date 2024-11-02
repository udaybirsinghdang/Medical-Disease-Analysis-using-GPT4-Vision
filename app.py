from openai import OpenAI
import streamlit as st
import base64
import os
from dotenv import load_dotenv
import tempfile
from src.helper import *


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

#print("OK")
#print(sample_prompt)

# Initializing session state variables
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
    
if "result" not in st.session_state:
    st.session_state.result = None 
    
#encode and decode image using base64
def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf8')
    
#eli explanation
def chat_eli(query):
    eli5_prompt = "Please explain the information like you explain a 5 year old. \n" + query
    messages =[
        {
            "role": "user",
            "content": eli5_prompt
        }
    ]
    
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages=messages,
        max_tokens=1500
    )


    
# GPT Functionality 
def call_gpt4_model_for_analysis(filename: str, sample_prompt =sample_prompt):
    base64_image = encode_image(filename)

    messages = [
        {
            "role": 'user',
            "content": [
                {
                    "type": "text", "text":sample_prompt
                },
                {
                    "type": "image_url",
                    "image_url":{
                        "url": f"data:image/jpeg:base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1500
    )
    
    print(response.choices[0].message.content)
    return response.choices[0].message.content


#Defining the User Experience using streamlit
st.title("Medical Disease Analysis")

with st.expander("About this Application"):
    st.write("Upload an image to analyze the disease using GPT-4 Vision")
    
uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

#Storing the file in a temp file
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        st.session_state['filename'] = temp_file.name
        
        st.image(uploaded_file, caption="Uploaded Image")
        

#Process Button
if st.button('Analyze Image'):
    if 'filename' in st.session_state and os.path.exists(st.session_state['filename']):
        print(st.session_state['filename'])
        st.session_state['result'] = call_gpt4_model_for_analysis(st.session_state['filename'])
        st.markdown(st.session_state['result'], unsafe_allow_html=True)
        os.unlink(st.session_state['filename']) #Delete the temp file after analyzing
        
        

#EL I5 Explanation
#print(st.session_state['result'])
#if 'result' in st.session_state and st.session_state['result']:
 #   st.info("Below you have an option to understand in simpler terms.")
  #  if st.radio("Explain like I'm 5", ('No', 'Yes')) == 'Yes':
   #     simplified_explanation = chat_eli(st.session_state['result'])
    #    st.markdown(simplified_explanation, unsafe_allow_html=True)