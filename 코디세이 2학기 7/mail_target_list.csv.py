import smtplib  # SMTP 프로토콜용 내장 패키지
import csv  # CSV 파일 처리를 위한 내장 패키지
from email.mime.text import MIMEText  # 메일 본문 구성용
from email.mime.multipart import MIMEMultipart  # 본문 + 첨부 가능 구조
from email.header import Header  # 제목 인코딩용


def send_mail_html():
    """CSV에 등록된 모든 대상에게 HTML 메일을 전송하는 함수"""

    # 1. 발신자 설정
    sender_email = '1234@gmail.com'
    sender_password = 'nfwp vsln zqqv ebal'

    # 2. SMTP 서버 정보
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # 3. CSV 파일에서 수신자 명단 읽기
    recipients = []
    try:
        with open('mail_target_list.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 첫 줄(헤더) 건너뜀
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    email = row[1].strip()
                    recipients.append((name, email))
    except FileNotFoundError:
        print('CSV 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print('CSV 파일 처리 중 오류 발생:', e)
        return

    # 4. SMTP 서버 연결 시도
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 또는 비밀번호를 확인하세요.')
        return
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다.')
        return
    except Exception as e:
        print('SMTP 연결 오류:', e)
        return

    # 5. 수신자별 메일 전송
    for name, email in recipients:
        subject = 'HTML 테스트 메일입니다.'
        # HTML 형식의 본문
        body_html = (
            f'<html>'
            f'<body>'
            f'<h2 style="color: blue;">안녕하세요, {name}님!</h2>'
            f'<p>이 메일은 Python을 이용한 <b>HTML 형식</b> 테스트 메일입니다.</p>'
            f'<p>즐거운 하루 되세요 😊</p>'
            f'</body>'
            f'</html>'
        )

        # MIMEMultipart 객체 구성
        message = MIMEMultipart('alternative')
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = Header(subject, 'utf-8')

        # HTML 본문 첨부
        message.attach(MIMEText(body_html, 'html', 'utf-8'))

        try:
            server.send_message(message)
            print(f'{name}({email}) 님에게 메일 전송 완료.')
        except smtplib.SMTPRecipientsRefused:
            print(f'{email} 주소가 유효하지 않습니다.')
        except Exception as e:
            print(f'{email} 전송 중 오류 발생:', e)

    # 6. 서버 연결 종료
    try:
        server.quit()
        print('모든 메일 전송 완료. 연결 종료.')
    except Exception:
        pass


if __name__ == '__main__':
    send_mail_html()
