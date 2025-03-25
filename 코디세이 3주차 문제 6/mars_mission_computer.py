import random

class DummySensor:
    """화성 기지 환경 센서의 더미 클래스"""

    def __init__(self):
        """초기 환경 값을 설정"""
        self.env_values = {}

    def set_env(self):
        """주어진 범위 내에서 무작위 값을 생성하여 env_values에 저장"""
        self.env_values = {
            'mars_base_internal_temperature': random.randint(18, 30),
            'mars_base_external_temperature': random.randint(0, 21),
            'mars_base_internal_humidity': random.randint(50, 60),
            'mars_base_external_illuminance': random.randint(500, 715),
            'mars_base_internal_Co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': random.randint(4, 7),
        }

    def get_env(self):
        """현재 환경 값을 반환"""
        return self.env_values

    def save_to_csv(self):
        """환경 값을 CSV 파일로 저장 (파일이 중복되지 않도록 자동 증가)"""
        file_index = 1

        while True:
            file_name = f'mars_bunker_{file_index}.csv'
            try:
                # 파일이 존재하는지 확인하기 위해 읽기 시도
                with open(file_name, 'r', encoding='utf-8'):
                    file_index += 1  # 존재하면 번호 증가
            except FileNotFoundError:
                break  # 존재하지 않으면 반복 종료

        # 새로운 파일에 환경 값 저장
        with open(file_name, 'w', encoding='utf-8') as file:
            for key, value in self.env_values.items():
                file.write(f'{key}, {value}\n')

        print(f'환경 데이터가 {file_name} 파일로 저장되었습니다.')

# 인스턴스 생성
ds = DummySensor()

# 환경 값 설정
ds.set_env()

# 환경 값 출력
print(ds.get_env())

# CSV 파일 저장
ds.save_to_csv()
