import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. AI 열쇠 설정 (사용자님의 키는 그대로 유지하세요)
genai.configure(api_key="AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ AI 데이터 정제 시스템")
st.write("사진을 올리면 글자를 읽어드립니다.")

uploaded_file = st.file_uploader("사진을 올려주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("✨ 데이터 추출"):
        with st.spinner('AI 분석 중...'):
            prompt = "이 이미지에서 날짜, 업체명, 총 금액을 찾아서 한글로 정리해줘."
            response = model.generate_content([prompt, img])
            st.success("추출 완료!")
            st.write(response.text)
