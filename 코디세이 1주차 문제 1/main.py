file_path = r'C:\Users\godzi\codyssey\mission_computer_main.log'

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()  # 파일 내용을 문자열로 반환
    except FileNotFoundError:
        return f'Error: 로그 파일을 찾을 수 없습니다. ({path})'
    except PermissionError:
        return f'Error: 로그 파일에 접근할 수 있는 권한이 없습니다. ({path})'
    except OSError as e:
        return f'Error: 로그 파일을 읽는 중 오류 발생 - {e}'

def print_file_content():
    content = read_file(file_path)
    print(content)

    if 'Error' not in content:
        print('로그 파일에 접속했습니다!!')

if __name__ == '__main__':
    print_file_content()
