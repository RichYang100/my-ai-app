from http.server import BaseHTTPRequestHandler
import json
import base64
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # 한글이 깨지지 않게 utf-8 설정을 확실히 합니다.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"></head>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif; line-height: 1.6;">
                <h1>🛡️ AI 데이터 정제 시스템 (완성판)</h1>
                <p>영수증이나 서류 사진을 올리면 AI가 즉시 분석합니다.</p>
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
            # 1. 사진 데이터 안전하게 가져오기
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            # 파일 데이터만 깔끔하게 분리
            try:
                img_part = body.split(b'\r\n\r\n')[1].split(b'\r\n--')[0]
                img_base64 = base64.b64encode(img_part).decode('utf-8')
            except:
                img_base64 = base64.b64encode(body).decode('utf-8')

            # 2. AI에게 물어보기
            api_key = "AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 이미지에서 날짜, 업체명, 품목, 총 금액을 찾아서 보기 좋게 한글로 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            # AI 답변 추출
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
            else:
                text = "AI 분석에 실패했습니다. 사진을 다시 확인해주세요."

            # 3. 결과 화면 보여주기 (한글 패치 완료)
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
            self.wfile.write(f"오류가 발생했습니다: {str(e)}".encode('utf-8'))
