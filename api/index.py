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
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f8f9fa;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50;">🛡️ 상업용 AI 정제기 v4</h2>
                    <p style="color: #7f8c8d;">영수증 사진을 올리면 즉시 분석을 시작합니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <button type="submit" style="width: 100%; background: #27ae60; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 지금 바로 추출하기</button>
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
            
            # 사진 데이터 추출
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_base64 = base64.b64encode(raw_body[header_end:footer_start]).decode('utf-8')

            api_key = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
            
            # [최종 수정 포인트] 버전 주소를 v1beta로 고정하여 호환성 문제를 원천 차단했습니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증 사진에서 날짜, 업체명, 품목, 총 금액을 찾아 한국어 표 형식으로 아주 정확하게 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status_text, color = "✅ 데이터 추출 성공", "#27ae60"
            else:
                # 에러 발생 시 구체적인 이유를 한글로 쉽게 보여줍니다.
                error_msg = result.get('error', {}).get('message', '연결 설정 재점검 필요')
                text = f"구글 AI 응답 확인: {error_msg}"
                status_text, color = "❌ 시스템 재점검", "#e74c3c"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            res_html = f"""
            <html><head><meta charset="utf-8"></head><body style="padding: 20px; font-family: sans-serif; background: #f8f9fa;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 15px;">
                    <h3 style="color: {color};">{status_text}</h3>
                    <div style="background:#f4f4f4; padding:20px; border-radius:10px; white-space: pre-wrap;">{text}</div>
                    <br><a href="/" style="text-decoration: none; color: #3498db; font-weight: bold;">← 다른 사진 올리기</a>
                </div>
            </body></html>
            """
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 긴급 로그: {str(e)}".encode('utf-8'))
