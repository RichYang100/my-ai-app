import os
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import base64

# 1. AI 엔진 설정 (구글 공식 방식)
API_KEY = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f8f9fa;">
                <div style="max-width: 450px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h2 style="color: #1a73e8;">🛡️ 상업용 AI 정제기 (표준형)</h2>
                    <p style="color: #5f6368;">구글 공식 라이브러리를 적용한 최종 안정화 버전입니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <button type="submit" style="width: 100%; background: #1a73e8; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 펀샵 영수증 테스트 시작</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 사진 데이터 수령
            content_length = int(self.headers['Content-Length'])
            raw_body = self.rfile.read(content_length)
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_data = raw_body[header_end:footer_start]

            # 2. AI 분석 실행 (공식 도구 사용으로 주소 오류 원천 차단)
            response = model.generate_content([
                "이 영수증 사진의 날짜, 업체명, 품목, 금액을 표로 아주 정확하게 정리해줘.",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            text = response.text
            status, color = "✅ 분석 성공", "#28a745"

        except Exception as e:
            text = f"분석 중 오류 발생: {str(e)}"
            status, color = "❌ 시스템 점검 필요", "#dc3545"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        res_html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px; font-family:sans-serif;'><h3>{status}</h3><div style='background:#eee;padding:20px;border-radius:10px;white-space:pre-wrap;'>{text}</div><br><a href='/'>← 다시 하기</a></body></html>"
        self.wfile.write(res_html.encode('utf-8'))
