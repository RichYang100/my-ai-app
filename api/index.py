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
            <body style="text-align: center; padding: 50px; font-family: sans-serif;">
                <h2>🛡️ AI 시스템 최종 점검</h2>
                <p>영수증 사진을 올려서 결과가 나오는지 확인하세요.</p>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">데이터 추출 테스트</button>
                </form>
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
            
            # [핵심 변경] v1beta 버전을 사용하고 모델명을 더 명확히 전달합니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증의 날짜, 업체명, 품목, 합계 금액을 한글로 추출해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            # 타임아웃을 설정하여 무한 대기를 방지합니다.
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
            else:
                # 구글의 실제 에러 메시지를 가감 없이 보여줍니다.
                text = f"구글 서버 응답: {json.dumps(result, ensure_ascii=False)}"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h3>✅ 테스트 결과</h3><pre style='background:#eee;padding:20px;'>{text}</pre><br><a href='/'>다시 시도</a>".encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"연결 오류: {str(e)}".encode('utf-8'))
