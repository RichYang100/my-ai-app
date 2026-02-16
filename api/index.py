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
            <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f9f9f9;">
                <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 15px; shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #333;">🛡️ AI 초정밀 데이터 정제기</h2>
                    <p style="color: #666;">영수증을 사진 찍어 올리면 엑셀 데이터로 변환합니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <br>
                        <button type="submit" style="background: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold;">추출 시작하기</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            raw_body = self.rfile.read(content_length)
            
            # 사진 데이터를 더 안정적으로 추출
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_part = raw_body[header_end:footer_start]
            img_base64 = base64.b64encode(img_part).decode('utf-8')

            # API 키 (사용자님의 키를 여기에 다시 한 번 정확히 넣어주세요)
            api_key = "AIzaSyDEYCVKTHAfa3KMD6mcg820mvg76NGbFHg"
            
            # [수정 포인트] API 호출 주소를 더 안정적인 v1 버전으로 변경
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증 사진에서 날짜, 업체명, 품목, 금액을 찾아서 한국어 표(Table) 형태로 아주 정확하게 정리해줘. 숫자는 콤마를 붙여서 출력해."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            # 헤더에 Content-Type 명시하여 오류 방지
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status = "success"
            else:
                # 에러 발생 시 구체적인 이유를 화면에 한글로 표시
                error_msg = result.get('error', {}).get('message', '알 수 없는 오류')
                text = f"AI 연결에 문제가 생겼습니다: {error_msg}"
                status = "error"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            res_html = f"""
            <html>
                <head><meta charset="utf-8"></head>
                <body style="padding: 20px; font-family: sans-serif; background: #f9f9f9;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px;">
                        <h3 style="color: {'#28a745' if status == 'success' else '#dc3545'};">{'✅ 분석 완료' if status == 'success' else '❌ 확인 필요'}</h3>
                        <div style="background:#eee; padding:15px; border-radius:5px; white-space: pre-wrap;">{text}</div>
                        <br><a href="/" style="text-decoration: none; color: #007bff;">← 돌아가기</a>
                    </div>
                </body>
            </html>
            """
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"서버 오류: {str(e)}".encode('utf-8'))
