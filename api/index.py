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
            <body style="text-align: center; padding: 50px; font-family: sans-serif; background: #f4f4f4;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2>🛡️ AI 시스템 최종 점검</h2>
                    <p>펀샵 영수증 사진을 올려서 테스트하세요.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required>
                        <br><br>
                        <button type="submit" style="padding: 10px 20px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px;">데이터 추출 테스트 시작</button>
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
            
            # [수정 핵심] 주소 체계를 v1beta가 아닌 가장 안정적인 v1 버전으로 맞췄습니다.
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증의 날짜, 업체명, 품목, 합계 금액을 한글 표로 정리해줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status = "✅ 테스트 성공"
            else:
                # 구글의 상세 에러를 분석하기 위해 원본을 출력합니다.
                text = f"구글 응답 메시지: {json.dumps(result, ensure_ascii=False)}"
                status = "❌ 시스템 재점검"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h3>{status}</h3><div style='background:#eee;padding:20px;white-space:pre-wrap;'>{text}</div><br><a href='/'>다시 시도</a>".encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"서버 긴급 오류: {str(e)}".encode('utf-8'))
