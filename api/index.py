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
                    <h2 style="color: #2c3e50;">🛡️ 상업용 AI 정제기 (최종)</h2>
                    <p style="color: #7f8c8d;">사장님은 사진만 찍으세요. 정리는 AI가 합니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <button type="submit" style="width: 100%; background: #27ae60; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 10초 만에 데이터 추출</button>
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
            
            # 사진 데이터 정밀 추출
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_base64 = base64.b64encode(raw_body[header_end:footer_start]).decode('utf-8')

            api_key = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
            
            # [수정포인트] v1beta와 gemini-1.5-flash 모델의 짝을 완벽하게 맞춘 최신 주소입니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증에서 날짜, 업체명, 품목, 금액을 찾아 표(Table)로 한국어 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status, color = "✅ 추출 성공", "#27ae60"
            else:
                # 에러 발생 시 원인을 한글로 상세히 보여줍니다.
                error_msg = result.get('error', {}).get('message', '연결 지연')
                text = f"구글 AI 응답 확인: {error_msg}"
                status, color = "❌ 재확인 필요", "#e74c3c"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            res_html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px;font-family:sans-serif;'><h3>{status}</h3><div style='background:#eee;padding:20px;border-radius:10px;white-space:pre-wrap;'>{text}</div><br><a href='/'>[다른 사진 올리기]</a></body></html>"
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 긴급 로그: {str(e)}".encode('utf-8'))
