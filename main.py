from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>🛡️ AI 데이터 정제 시스템 가동 중!</h1>
                <p>이제 아래 버튼을 눌러 서류 사진을 업로드하세요.</p>
                <form action="/api/main" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <button type="submit">데이터 추출하기</button>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        return
