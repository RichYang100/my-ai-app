from http.server import BaseHTTPRequestHandler
import json, base64, requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f0f2f5;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h2 style="color: #1a73e8;">🛡️ AI 영수증 마스터</h2>
                    <p style="color: #5f6368;">사진을 올리면 엑셀 데이터를 만듭니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0; font-size: 14px;">
                        <button type="submit" style="width: 100%; background: #1a73e8; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 데이터 추출 시작</button>
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
            
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_base64 = base64.b64encode(raw_body[header_end:footer_start]).decode('utf-8')

            # [필독] 새로 복사한 API 키를 아래 따옴표 안에 빈칸 없이 붙여넣으세요!
            api_key = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
            
            # 주소 끝에 'key=' 부분을 더 명확하게 처리했습니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증에서 날짜, 업체명, 품목, 금액을 표로 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            # 구글이 요구하는 정석 헤더와 키 전달 방식입니다.
            headers = {'Content-Type': 'application/json', 'x-goog-api-key': api_key}
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status_text = "✅ 분석 성공"
                color = "#28a745"
            else:
                text = f"구글 AI 응답 에러내용: {json.dumps(result, ensure_ascii=False)}"
                status_text = "❌ 설정 확인 필요"
                color = "#dc3545"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            res_html = f"""
            <html><head><meta charset="utf-8"></head><body style="padding: 20px; font-family: sans-serif;">
                <h3 style="color: {color};">{status_text}</h3>
                <div style="background:#eee; padding:20px; border-radius:10px; white-space: pre-wrap;">{text}</div>
                <br><a href="/">[처음으로 돌아가기]</a>
            </body></html>
            """
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"긴급 시스템 오류: {str(e)}".encode('utf-8'))
