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
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>🛡️ AI 데이터 정제기 (클린 버전)</h1>
                <p>영수증 사진을 올리면 AI가 즉시 분석합니다.</p>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit" style="padding: 10px 20px;">데이터 추출하기</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 사진 데이터를 안전하게 읽어오는 방식
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            # 실제 사진 데이터만 추출 (앞부분의 불필요한 정보 제거)
            img_data = base64.b64encode(body.split(b'\r\n\r\n')[1].split(b'\r\n--')[0]).decode('utf-8')
            
            api_key = "AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 이미지에서 날짜, 업체명, 총 금액을 찾아서 한글로 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h2>✅ 추출 결과</h2><pre style='background:#f4f4f4;padding:20px;'>{text}</pre><br><a href='/'>[다시 하기]</a>".encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"오류가 발생했지만 화면은 띄웁니다: {str(e)}".encode('utf-8'))
