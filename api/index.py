import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import cgi

# 구글 공식 설정 방식 (주소 오류를 원천 차단합니다)
API_KEY = "AIzaSyB0PX-lswkXVZtPJHr6D0zO1SSy7AEOpd8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <body style="text-align: center; padding: 50px; font-family: sans-serif;">
                <h2>🛡️ AI 정제기 (표준 라이브러리 버전)</h2>
                <p>구글 공식 도구를 사용하여 연결 안정성을 확보했습니다.</p>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">데이터 추출 시작</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            # 1. 사진 데이터 수령
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            file_item = form['file']
            img_data = file_item.file.read()

            # 2. 구글 공식 라이브러리로 AI 분석 (주소를 적지 않아도 알아서 찾아갑니다)
            response = model.generate_content([
                "이 영수증의 날짜, 업체명, 품목, 합계 금액을 한글 표로 정리해줘.",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            text = response.text
            status = "✅ 분석 성공"

        except Exception as e:
            text = f"분석 오류: {str(e)}"
            status = "❌ 점검 필요"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<h3>{status}</h3><div style='background:#eee;padding:20px;white-space:pre-wrap;'>{text}</div><br><a href='/'>돌아가기</a>".encode('utf-8'))
