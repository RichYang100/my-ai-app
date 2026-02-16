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
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f4f7f6;">
                <div style="max-width: 450px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50; margin-bottom: 10px;">🛡️ AI 영수증 마스터</h2>
                    <p style="color: #7f8c8d; font-size: 14px;">사장님은 사진만 찍으세요. 정리는 AI가 합니다.</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 25px 0;">
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin-bottom: 20px; font-size: 14px;">
                        <button type="submit" style="width: 100%; background: #27ae60; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold;">📊 10초 만에 엑셀 데이터 추출</button>
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

            # [중요] 새로 발급받은 API 키를 아래 따옴표 안에 꼭 '공백 없이' 넣어주세요!
            api_key = "여기에_새로_받은_키를_넣으세요"
            
            # 최신 안정화 버전(v1) 주소 사용
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "이 영수증에서 날짜, 업체명, 품목, 금액을 표로 정리해줘."},
                             {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}]
                }]
            }
            
            # 구글이 요구하는 표준 헤더 추가
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                color, status = "#27ae60", "✅ 분석 성공"
            else:
                text = f"구글 AI 응답 확인: {json.dumps(result)}"
                color, status = "#e74c3c", "❌ 설정 확인 필요"

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            res_html = f"""
            <html><head><meta charset="utf-8"></head><body style="padding: 20px; font-family: sans-serif; background: #f4f7f6;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 15px;">
                    <h3 style="color: {color};">{status}</h3>
                    <div style="background:#f9f9f9; padding:20px; border-radius:10px; white-space: pre-wrap; font-size: 14px; line-height: 1.6;">{text}</div>
                    <br><a href="/" style="color: #3498db; text-decoration: none; font-weight: bold;">← 다시 시도하기</a>
                </div>
            </body></html>
            """
            self.wfile.write(res_html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"시스템 긴급 확인: {str(e)}".encode('utf-8'))
