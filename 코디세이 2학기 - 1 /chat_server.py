# chat_server.py
import socket
import threading

# 접속된 클라이언트를 저장하는 리스트
clients = []
nicknames = []

# 클라이언트에게 메시지를 전체 전송하는 함수
def broadcast(message, sender=None):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            pass

# 클라이언트 개별 처리 스레드
def handle_client(client, addr):
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)

    # 입장 알림
    broadcast(f'{nickname}님이 입장하셨습니다.')

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '/종료':
                # 종료 처리
                clients.remove(client)
                nicknames.remove(nickname)
                broadcast(f'{nickname}님이 퇴장하셨습니다.')
                client.close()
                break
            else:
                broadcast(f'{nickname}> {message}')
        except:
            # 예외 시 연결 종료
            if client in clients:
                clients.remove(client)
            if nickname in nicknames:
                nicknames.remove(nickname)
            broadcast(f'{nickname}님이 연결이 끊어졌습니다.')
            client.close()
            break

# 서버 실행 부분
def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f'채팅 서버 시작: {host}:{port}')

    while True:
        client, addr = server.accept()
        print(f'{addr}에서 접속')
        # 새로운 스레드로 클라이언트 처리
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
