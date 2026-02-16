import streamlit as st
import google.generativeai as genai

# 1. AI 열쇠 설정 (사용자님의 키)
genai.configure(api_key="AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ 초간편 AI 데이터 정제")
st.write("이미지를 올리면 AI가 내용을 읽어드립니다.")

# 2. 사진 올리기
uploaded_file = st.file_uploader("사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # 이미지를 화면에 보여주기
    st.image(uploaded_file, width=300)
    
    if st.button("✨ 데이터 추출하기"):
        with st.spinner('분석 중...'):
            # 파일을 직접 읽어서 AI에게 전달
            img_data = uploaded_file.getvalue()
            response = model.generate_content([
                "이 이미지에서 날짜, 업체명, 총 금액을 찾아서 한글로 정리해줘.",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            st.success("완료!")
            st.write(response.text)
