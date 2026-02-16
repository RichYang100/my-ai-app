import os
from groq import Groq
from http.server import BaseHTTPRequestHandler
import cgi
import base64

# 1. Groq 엔진 설정 (사용자님의 새 API 키를 아래에 넣으세요)
client = Groq(api_key="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")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
            <head>
                <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { text-align: center; padding: 50px 20px; font-family: sans-serif; background: #f4f7f6; }
                    .card { max-width: 450px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
                    h2 { color: #2c3e50; }
                    input[type=file] { margin: 20px 0; }
                    button { width: 100%; background: #000; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; font-weight: bold; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>🛡️ 상업용 AI 정제기 (Groq)</h2>
                    <p>3시간의 구글 오류를 뚫어낸 초고속 버전입니다.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required>
                        <button type="submit">📊 펀샵 영수증 분석하기</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        try:
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            img_data = form['file'].file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')

            # Groq의 최신 비전 모델(Llama-3.2)을 사용하여 영수증을 분석합니다.
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 영수증 사진의 날짜, 업체명, 품목, 금액을 표(Table) 형식으로 아주 정확하게 정리해줘. 한국어로 대답해."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }],
                temperature=0.1
            )
            
            text = completion.choices[0].message.content
            status, color = "✅ 데이터 추출 성공", "#27ae60"

        except Exception as e:
            text = f"분석 오류: {str(e)}"
            status, color = "❌ 다시 시도해주세요", "#e74c3c"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        res_html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px; font-family:sans-serif;'><h3>{status}</h3><div style='background:#f1f3f4;padding:20px;border-radius:10px;white-space:pre-wrap;'>{text}</div><br><a href='/'>← 돌아가기</a></body></html>"
        self.wfile.write(res_html.encode('utf-8'))
