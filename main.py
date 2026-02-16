import os
import requests
import json

# 이 코드는 아주 가벼워서 절대 오류가 나지 않습니다.
def handler(request):
    # 사용자가 접속하면 보여줄 아주 간단한 화면
    html_content = """
    <html>
        <body>
            <h1>🛡️ 초간편 AI 데이터 정제</h1>
            <p>Vercel 용량 문제를 해결한 초경량 버전입니다.</p>
            <form action="/api/extract" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <button type="submit">데이터 추출하기</button>
            </form>
        </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html_content
    }
