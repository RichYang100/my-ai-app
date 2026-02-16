from http.server import BaseHTTPRequestHandler
import cgi
import requests
import json

class handler(BaseHTTPRequestHandler):
    # 1. 화면 보여주기
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>🛡️ AI 데이터 정제 시스템 가동 중!</h1>
                <p>이제 아래 버튼을 눌러 서류 사진을 업로드하세요.</p>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <button type="submit">데이터 추출하기</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    # 2. 사진 받아서 AI에게 물어보기 (이 부분이 추가되었습니다!)
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        file_item = form['file']
        
        # AI에게 물어볼 비밀번호와 주소
        api_key = "AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # 사진 데이터를 AI가 이해할 수 있게 변환
        import base64
        img_data = base64.b64encode(file_item.file.read()).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "이 이미지에서 날짜, 업체명, 총 금액을 찾아서 한글로 정리해줘."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                ]
            }]
        }
        
        # AI에게 전송 및 결과 받기
        response = requests.post(url, json=payload)
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']

        # 결과 화면 보여주기
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<h2>✅ 추출 결과</h2><pre>{text}</pre><br><a href='/'>다시 하기</a>".encode('utf-8'))
