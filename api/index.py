from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>🛡️ AI 데이터 정제 시스템이 준비되었습니다!</h1>
                <p>파일을 선택해서 업로드하면 AI가 분석을 시작합니다.</p>
                <form action="/api/index" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <button type="submit">데이터 추출하기</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        return
