import streamlit as st
import os
import io
from dotenv import load_dotenv
import google.generativeai as gen_ai
import google.ai.generativelanguage as glm
from PIL import Image
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="MoneyMaven Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

with st.sidebar:
    selected = option_menu(
        menu_title="MoneyMaven Dashboard",
        options=["Stock Dashboard", "MoneyMaven Chatbot"],
        icons=["bar-chart", "robot"],
        default_index=0,
        orientation="vertical",
    )

    if selected == "Stock Dashboard":
        st.write("📈 **Track stocks, analyze trends, and stay informed.**")
    elif selected == "MoneyMaven Chatbot":
        st.write("🤖 **Chat with MoneyMaven for finance insights.**")

if selected == "Stock Dashboard":
    st.title("📊 MoneyMaven Stock Dashboard")
    st.write("(Placeholder for stock data, analysis tools, and market insights)")
    
    # Add stock-related content (e.g., stock prices, news, analytics)
    st.write("Feature development in progress...")

elif selected == "MoneyMaven Chatbot":
    st.title("💬 Chat with MoneyMaven™")
    
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    user_prompt = st.chat_input("Ask MoneyMaven anything about finance...")
    
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    
    st.header("📷 VisionBot™ (Finance Image Analysis)")
    image_prompt = st.text_input("Describe what you want to analyze in an image", placeholder="e.g., Analyze this stock chart")
    uploaded_file = st.file_uploader("Upload a financial chart or image", type=["png", "jpg", "jpeg", "webp"])
    
    if uploaded_file is not None:
        st.image(Image.open(uploaded_file), use_column_width=True)
        
    if st.button("Analyze Image"):
        model = gen_ai.GenerativeModel("gemini-1.5-flash")
        
        if uploaded_file is not None and image_prompt:
            image = Image.open(uploaded_file)
            response = model.generate_content([image_prompt, image])
            st.write("📢 **Analysis Result:**")
            st.markdown(response.text)
        else:
            st.error("Please provide both an image and a prompt.")
