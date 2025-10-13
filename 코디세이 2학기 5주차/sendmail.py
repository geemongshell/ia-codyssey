import smtplib  # SMTP 프로토콜을 위한 내장 패키지
from email.mime.text import MIMEText  # 메일 본문 구성용
from email.mime.multipart import MIMEMultipart  # 첨부 가능 구조
from email.header import Header  # 메일 제목 인코딩용


def send_mail():
    #Gmail SMTP를 이용하여 메일을 보내는 함수

        # 1. 메일 기본 설정
    
    sender_email = '123445@gmail.com'
    sender_password = '네에글자 4글자아 네개글자 끼요오옷'
    receiver_email = '543234naver.com'

    
    # 2. 메일 제목과 본문 구성
    
    subject = '크하하하하하핳'
    body = '끼요오오오오오오오옷!!!'

    # MIMEMultipart 객체 생성 (본문 + 제목 + 수신자 정보 등 설정 가능)
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = Header(subject, 'utf-8')

    # 메일 본문 추가
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    
    # 3. SMTP 서버 설정
    
    smtp_server = 'smtp.gmail.com'  # Gmail SMTP 서버 주소
    smtp_port = 587  # TLS 포트 (기본: 587)

    try:
        # SMTP 객체 생성 및 서버 연결
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # 서버와 인사
        server.starttls()  # TLS(보안 연결) 시작
        server.login(sender_email, sender_password)  # 로그인

        
        # 4. 메일 전송
        
        server.send_message(message)
        print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 또는 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다.')
    except smtplib.SMTPException as e:
        print('SMTP 예외 발생:', e)
    except Exception as e:
        print('기타 오류 발생:', e)
    finally:
        
        # 5. 연결 종료
        
        try:
            server.quit()
        except Exception:
            pass


if __name__ == '__main__':
    send_mail()
