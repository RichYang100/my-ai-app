from http.server import BaseHTTPRequestHandler
import json, base64, requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"></head>
            <body style="text-align: center; padding: 50px; font-family: sans-serif; background: #f0f4f7;">
                <div style="max-width: 450px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <h2 style="color: #2c3e50;">🛡️ 상업용 AI 정제기 (완성형)</h2>
                    <p style="color: #7f8c8d;">영수증 사진을 올려서 테스트를 완료하세요.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <br>
                        <button type="submit" style="background: #1a73e8; color: white; border: none; padding: 12px 30px; border-radius: 8px; cursor: pointer; font-weight: bold;">📊 즉시 데이터 추출</button>
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
            
            # 사진 데이터 추출 로직 강화
            header_end = raw_body.find(b'\r\n\r\n') + 4
            footer_start = raw_body.rfind(b'\r\n--')
            img_base64 = base64.b64encode(raw_body[header_end:footer_start]).decode('utf-8')

            api_key = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
            
            # [최종 해결책] 주소를 v1beta로, 모델명을 정식 명칭으로 정확히 매칭했습니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증 사진의 업체명, 품목, 금액을 표 형식으로 아주 정확하게 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status, color = "✅ 테스트 성공", "#2ecc71"
            else:
                error_msg = result.get('error', {}).get('message', '연결 지연')
                text = f"구글 AI 응답 확인: {error_msg}"
                status, color = "❌ 재확인 필요", "#e74c3c"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h3>{status}</h3><div style='background:#f8f9fa;padding:20px;white-space:pre-wrap;border-radius:10px;'>{text}</div><br><a href='/'>← 돌아가기</a>".encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 긴급 진단: {str(e)}".encode('utf-8'))
