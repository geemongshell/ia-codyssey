# door_hacking.py
import zipfile
import time
import itertools
import zlib


def unlock_zip():
    """
    Brute-force로 zip 파일 'emergency_storage_key.zip'의 암호를 푸는 함수.
    - 암호는 소문자와 숫자로 구성된 8자리 문자열.
    - 성공 시 암호를 'password.txt'에 저장하고, 시작 시간, 반복 횟수, 경과 시간을 출력.
    - zip 파일이 없거나 오류 발생 시 예외 처리 수행.
    - 5분마다 경과 시간과 현재 시도 중인 자리 수를 출력하여 진행 상태를 확인.
    """
    start_time = time.time()  # 시작 시간 기록
    last_report_time = start_time  # 마지막 경과 시간 출력 시간
    report_interval = 300  # 5분(300초)마다 진행 상태 출력
    attempts = 0  # 시도 횟수
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'  # 암호에 사용할 문자 집합

    try:
        with zipfile.ZipFile('emergency_storage_key.zip', 'r') as zip_file:
            # 가능한 모든 8자리 조합을 생성하여 시도
            for password in itertools.product(charset, repeat=8):
                attempts += 1
                password = ''.join(password).encode('utf-8')  # 암호 조합을 문자열로 변환 후 바이트로 인코딩

                # 5분마다 진행 상태 출력
                current_time = time.time()
                if current_time - last_report_time >= report_interval:
                    elapsed_time = current_time - start_time
                    # 암호 진행 상태를 표시 (현재까지 시도한 자리까지만 표시)
                    decoded_password = password.decode('utf-8')
                    progress = ''.join([c if i < len(decoded_password) else '*' for i, c in enumerate(decoded_password)])
                    print(f"[INFO] Elapsed time: {elapsed_time / 60:.2f} minutes")
                    print(f"[INFO] Attempts: {attempts}, Current progress: {progress}")
                    last_report_time = current_time

                try:
                    # 추출 시도
                    zip_file.extractall(pwd=password)
                    elapsed_time = time.time() - start_time
                    print(f"[SUCCESS] Password found: {password.decode('utf-8')}")
                    print(f"Attempts: {attempts}")
                    print(f"Elapsed time: {elapsed_time:.2f} seconds")
                    # 성공한 암호를 파일로 저장
                    with open('password.txt', 'w') as f:
                        f.write(password.decode('utf-8'))
                    return
                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    # 암호가 틀린 경우 혹은 압축 해제 중 오류 발생 시 무시하고 다음 시도로 진행
                    continue
        print("[FAILED] Password not found.")
    except FileNotFoundError:
        print("[ERROR] Zip file not found.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == '__main__':
    print("[INFO] Starting the brute-force password cracking...")
    unlock_zip()
