import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
        except:
            break

def start_client(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    nickname = input('닉네임 입력: ')
    client.send(nickname.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input()
        client.send(msg.encode('utf-8'))
        if msg == '/종료':
            client.close()
            break

if __name__ == '__main__':
    start_client()
