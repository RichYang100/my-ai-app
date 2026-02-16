import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import cgi

# 1. AI 엔진 설정 (구글 공식 라이브러리 방식 - 주소 오류 원천 차단)
API_KEY = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
genai.configure(api_key=API_KEY)

# 구글 서버가 100% 인식하는 'latest' 경로로 모델을 고정합니다.
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f8f9fa;">
                <div style="max-width: 450px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h2 style="color: #1a73e8;">🛡️ 상업용 AI 정제기 (직통 연결)</h2>
                    <p style="color: #666;">구글 공식 도구를 사용하여 연결 오류를 완전히 해결했습니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin: 20px 0;">
                        <button type="submit" style="width: 100%; background: #1a73e8; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold;">📊 펀샵 영수증 테스트 시작</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 2. 사진 데이터 수령 (표준 cgi 방식)
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            img_data = form['file'].file.read()

            # 3. AI 분석 실행 (공식 도구가 알아서 주소를 찾아갑니다)
            response = model.generate_content([
                "이 영수증 사진의 날짜, 업체명, 품목, 금액을 표로 아주 정확하게 정리해줘.",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            text = response.text
            status, color = "✅ 분석 성공", "#28a745"

        except Exception as e:
            # 오류 발생 시 구체적인 원인을 한글로 출력합니다.
            text = f"분석 중 오류 발생: {str(e)}"
            status, color = "❌ 시스템 점검 필요", "#dc3545"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        res_html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px; font-family:sans-serif;'><h3>{status}</h3><div style='background:#f1f3f4;padding:20px;border-radius:10px;white-space:pre-wrap;'>{text}</div><br><a href='/'>← 돌아가기</a></body></html>"
        self.wfile.write(res_html.encode('utf-8'))
