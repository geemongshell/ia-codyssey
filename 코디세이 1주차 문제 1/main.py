# 파일 경로를 지정 (절대 경로 사용)
file_path = r'C:\Users\godzi\codyssey\mission_computer_main.log'

def read_file(path):
    """
    지정된 경로의 파일을 읽고 내용을 반환하는 함수.
    파일이 존재하지 않거나 접근할 수 없을 경우, 적절한 오류 메시지를 반환.
    
    :param path: 읽을 파일의 경로 (문자열)
    :return: 파일 내용 (문자열) 또는 오류 메시지 (문자열)
    """
    try:
        # UTF-8 인코딩으로 파일을 읽기 모드('r')로 열기
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()  # 파일 내용을 문자열로 반환
    except FileNotFoundError:
        # 파일이 존재하지 않을 때 예외 처리
        return f'Error: 로그 파일을 찾을 수 없습니다. ({path})'
    except PermissionError:
        # 파일에 접근할 권한이 없을 때 예외 처리
        return f'Error: 로그 파일에 접근할 수 있는 권한이 없습니다. ({path})'
    except OSError as e:
        # 기타 파일 관련 오류 처리 (예: 디스크 오류, 경로 문제 등)
        return f'Error: 로그 파일을 읽는 중 오류 발생 - {e}'

def print_file_content():
    """
    파일 내용을 읽고 화면에 출력하는 함수.
    파일을 정상적으로 읽었으면 '로그 파일에 접속했습니다!!' 메시지 출력.
    """
    content = read_file(file_path)  # read_file() 함수를 호출하여 파일 내용 가져오기
    print(content)  # 파일 내용 또는 오류 메시지를 출력

    # 파일을 정상적으로 읽은 경우, '로그에 접속했습니다!!' 메시지 출력
    if 'Error' not in content:
        print('로그 파일에 접속했습니다!!')

# 스크립트가 직접 실행될 경우, print_file_content() 실행
if __name__ == '__main__':
    print_file_content()
