# 카이사르 암호를 해독하는 함수 정의
def caesar_cipher_decode(target_text):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    length = len(alphabet)

    print('--- 카이사르 해독 결과 ---')
    for shift in range(length):
        decoded = ''
        for char in target_text:
            if char in alphabet:
                index = alphabet.index(char)
                decoded += alphabet[(index - shift) % length]
            elif char in alphabet.upper():
                index = alphabet.upper().index(char)
                decoded += alphabet.upper()[(index - shift) % length]
            else:
                decoded += char
        print(f'[{shift}] {decoded}')

# password.txt 파일 읽기
def read_password():
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다: password.txt')
        return ''
    except Exception as e:
        print('파일을 읽는 중 오류가 발생했습니다:', e)
        return ''

# result.txt에 저장하기
def save_result(result_text):
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(result_text)
        print('결과가 result.txt에 저장되었습니다.')
    except Exception as e:
        print('결과 저장 중 오류가 발생했습니다:', e)

# 실행 로직
def main():
    encrypted_text = read_password()
    if not encrypted_text:
        return

    caesar_cipher_decode(encrypted_text)

    print('\n해독된 번호를 입력하세요 (0~25):')
    try:
        shift = int(input('>> '))
        if 0 <= shift <= 25:
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            result = ''
            for char in encrypted_text:
                if char in alphabet:
                    index = alphabet.index(char)
                    result += alphabet[(index - shift) % 26]
                elif char in alphabet.upper():
                    index = alphabet.upper().index(char)
                    result += alphabet.upper()[(index - shift) % 26]
                else:
                    result += char
            save_result(result)
        else:
            print('0에서 25 사이의 숫자를 입력해야 합니다.')
    except ValueError:
        print('숫자를 입력해주세요.')

if __name__ == '__main__':
    main()
