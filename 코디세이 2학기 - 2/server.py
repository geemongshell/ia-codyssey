from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class Spaceman(BaseHTTPRequestHandler):
    # 클라이언트 요청 처리 메서드
    def do_GET(self):
        # index.html 파일 읽기
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = '<html><body><h1>index.html 파일을 찾을 수 없습니다.</h1></body></html>'

        # 응답 상태 코드 (200 OK)
        self.send_response(200)

        # 헤더 전송 (캐시 방지 옵션 포함)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

        # 클라이언트에 HTML 전송
        self.wfile.write(content.encode('utf-8'))

        # 서버 콘솔에 접속 정보 출력
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        print(f'[{now}] 클라이언트 접속: {client_ip}', flush=True)


def run_server():
    host = ('', 8080)  # 모든 인터페이스에서 8080 포트 대기
    httpd = HTTPServer(host, Spaceman)
    print('HTTP 서버 실행 중이여 (포트 8080)...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
