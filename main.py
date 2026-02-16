import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

genai.configure(api_key="AIzaSyDEYCVKTHAFa3KMD6mcg820mvg76NGbFHg")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ AI 데이터 정제 시스템")
uploaded_file = st.file_uploader("사진을 올려주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    if st.button("✨ 데이터 추출"):
        prompt = "이 이미지에서 날짜, 업체명, 총 금액을 JSON 형식으로 추출해줘."
        response = model.generate_content([prompt, img])
        st.write(response.text)
