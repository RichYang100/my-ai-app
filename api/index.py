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
            <body style="text-align: center; padding: 50px; font-family: sans-serif; background: #f4f7f6;">
                <div style="max-width: 450px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50;">🛡️ 상업용 AI 정제기 (우회 버전)</h2>
                    <p style="color: #7f8c8d;">펀샵 영수증 사진을 올려서 마지막 테스트를 완료하세요.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <button type="submit" style="width: 100%; background: #27ae60; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 즉시 데이터 추출 시작</button>
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
            
            # [최종 해결책] 주소를 v1beta로, 모델명을 'models/gemini-1.5-flash-latest'로 명확히 지정했습니다.
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "이 영수증 사진의 업체명, 품목, 금액을 표(Table)로 한국어 정리해줘. 결과만 깔끔하게 보여줘."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                    ]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload, timeout=40)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                status, color = "✅ 데이터 추출 성공", "#27ae60"
            else:
                # 구글의 상세 응답을 분석하기 위해 그대로 출력합니다.
                text = f"구글 AI 응답 확인: {json.dumps(result, ensure_ascii=False)}"
                status, color = "❌ 재확인 필요", "#e74c3c"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            res_html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px;font-family:sans-serif;'><h3>{status}</h3><div style='background:#eee;padding:20px;border-radius:10px;white-space:pre-wrap;'>{text}</div><br><a href='/'>← 돌아가기</a></body></html>"
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 긴급 진단: {str(e)}".encode('utf-8'))
