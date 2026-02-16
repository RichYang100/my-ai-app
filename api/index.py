from http.server import BaseHTTPRequestHandler
import json
import base64
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"></head>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>🛡️ AI 데이터 정제 시스템 (가동 중)</h1>
                <p>영수증 사진을 올리면 AI가 즉시 분석합니다.</p>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit" style="padding: 10px 20px; cursor: pointer;">데이터 추출 시작</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 1. 원본 데이터 읽기
            content_length = int(self.headers['Content-Length'])
            raw_body = self.rfile.read(content_length)
            
            # 2. 이미지 데이터만 추출 (더 정교하게 수정)
            try:
                # 파일 업로드 시 섞여 들어오는 문자열 데이터들을 제거하고 순수 이미지 바이트만 찾습니다.
                header_end = raw_body.find(b'\r\n\r\n') + 4
                footer_start = raw_body.rfind(b'\r\n--')
                img_part = raw_body[header_end:footer_start]
                img_base64 = base64.b64encode(img_part).decode('utf-8')
            except:
                img_base64 = base64.b64encode(raw_body).decode('utf-8')

            # 3. Gemini AI에게 전달
            api_key = "AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 이미지에서 날짜, 업체명, 품목명, 단가, 수량, 총 금액을 찾아서 한국어 표 형식으로 깔끔하게 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
            else:
                # 오류 시 AI의 원본 응답을 보여줘서 문제를 파악합니다.
                text = f"AI 응답 오류: {json.dumps(result)}"

            # 4. 결과 출력
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            result_html = f"""
            <html>
                <head><meta charset="utf-8"></head>
                <body style="padding: 20px; font-family: sans-serif;">
                    <h2>✅ AI 분석 결과</h2>
                    <div style="background:#f4f4f4; padding:20px; border-radius:10px; white-space: pre-wrap;">{text}</div>
                    <br><a href='/'>[다른 사진 올리기]</a>
                </body>
            </html>
            """
            self.wfile.write(result_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 오류 발생: {str(e)}".encode('utf-8'))
