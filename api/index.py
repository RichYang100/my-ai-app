import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import cgi

# 1. AI 엔진 설정 (가장 안정적인 v1 API 키 방식)
API_KEY = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        # 깔끔하고 직관적인 업로드 화면
        html = """
        <html>
            <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="text-align: center; padding: 50px; font-family: sans-serif; background: #f0f4f8;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #1a73e8;">🛡️ AI 정제기 (최종 연결형)</h2>
                    <p>펀샵 영수증 사진을 올려서 테스트하세요.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required style="margin-bottom: 20px;">
                        <button type="submit" style="width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 8px; cursor: pointer;">데이터 추출 확인</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 2. 사진 데이터 수령 (표준 방식)
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            img_data = form['file'].file.read()

            # 3. AI 분석 (주소 오류를 피하기 위해 라이브러리 직접 호출)
            response = model.generate_content([
                "이 사진의 날짜, 업체명, 품목, 금액을 한글 표로 정리해줘.",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            result_text = response.text
            status_text = "✅ 테스트 성공"

        except Exception as e:
            result_text = f"연결 확인 필요: {str(e)}"
            status_text = "❌ 재확인 필요"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        res_html = f"<html><body style='padding:20px; font-family:sans-serif;'><h3>{status_text}</h3><div style='background:#eee;padding:20px;border-radius:10px;white-space:pre-wrap;'>{result_text}</div><br><a href='/'>[다시 하기]</a></body></html>"
        self.wfile.write(res_html.encode('utf-8'))
