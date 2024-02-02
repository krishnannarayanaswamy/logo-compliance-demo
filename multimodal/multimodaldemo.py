import streamlit as st
from PIL import Image as PIL_Image
import http.client
import typing
import urllib.request
#import google.generativeai as genai
#from vertexai.preview.generative_models import Part
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Image,
    Part,
)

def get_image_bytes_from_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        image_bytes = response.read()
    return image_bytes

def load_image_from_url(image_url: str) -> Image:
    image_bytes = get_image_bytes_from_url(image_url)
    return Image.from_bytes(image_bytes)

st.set_page_config(page_title="Gemini Pro Multimodal Processor")

st.write("Welcome to the Gemini Pro Multimodal Processor. You can proceed by providing your Google API Key")

#with st.expander("Provide Your Google API Key"):
#     google_api_key = st.text_input("Google API Key", key="google_api_key", type="password")
     
#if not google_api_key:
#    st.info("Enter the Google API Key to continue")
#    st.stop()

#genai.configure(api_key=google_api_key)

st.title("Gemini Pro Multimodal Processor")

with st.sidebar:
    option = st.selectbox('Choose Your Model',('gemini-pro', 'gemini-pro-vision'))

    if 'model' not in st.session_state or st.session_state.model != option:
        st.session_state.chat = GenerativeModel(option).start_chat(history=[])
        st.session_state.model = option
    
    st.write("Adjust Your Parameter Here:")
    temperature = st.number_input("Temperature", min_value=0.0, max_value= 1.0, value =0.5, step =0.01)
    max_token = st.number_input("Maximum Output Token", min_value=0, value =100)
    gen_config = GenerationConfig(max_output_tokens=max_token,temperature=temperature)
    
    st.divider()
    
    #upload_image = st.file_uploader("Upload Your Image Here", accept_multiple_files=False, type = ['jpg', 'png'])
    upload_image =  st.text_input("Enter Your Image URL Here")
    if upload_image:
        image = load_image_from_url(upload_image)
    st.divider()

    upload_video =  st.text_input("Enter Your Video URL Here")
    if upload_video:
        video = Part.from_uri(
            uri=upload_video,
            mime_type="video/mp4",
        )
    st.divider()

    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if upload_video:
    if option == "gemini-pro":
        st.info("Please Switch to the Gemini Pro Vision")
        st.stop()
    if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            #response=st.session_state.chat.send_message([prompt,video],stream=True,generation_config = gen_config)
            responses=GenerativeModel(option).generate_content([prompt,video],stream=True,generation_config = gen_config)
            #response.resolve()
            #msg = response.text
            messages = ""
            for response in responses:
                print(response.text, end="")
                messages = messages + response.text
            msg=messages    
            
            st.session_state.chat = GenerativeModel(option).start_chat(history=[])
            st.session_state.messages.append({"role": "assistant", "content": msg})

            st.chat_message("assistant").write(msg)
elif upload_image:
    if option == "gemini-pro":
        st.info("Please Switch to the Gemini Pro Vision")
        st.stop()
    if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            #response=st.session_state.chat.send_message([prompt,image],stream=True,generation_config = gen_config)
            responses=GenerativeModel(option).generate_content([prompt,image],stream=True,generation_config = gen_config)
            #response.resolve()
            #msg=response.text
            messages = ""
            for response in responses:
                print(response.text, end="")
                messages = messages + response.text
            msg=messages  
            #print(responses.text)
            #msg=responses.text

            st.session_state.chat = GenerativeModel(option).start_chat(history=[])
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
            #st.image(image,width=300)
            st.chat_message("assistant").write(msg)

else:
    if prompt := st.chat_input():
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            #responses=st.session_state.chat.send_message(prompt,stream=True,generation_config = gen_config)
            responses=GenerativeModel(option).generate_content(prompt,stream=True,generation_config = gen_config)
            #response.resolve()
            #msg=response.text
            messages = ""
            for response in responses:
                print(response.text, end="")
                messages = messages + response.text
            msg=messages  
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
    
    