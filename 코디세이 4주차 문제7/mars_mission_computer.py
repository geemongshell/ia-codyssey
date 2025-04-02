import random
import time
import json

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

class MissionComputer:
    """미션 컴퓨터 클래스"""

    def __init__(self):
        """센서 인스턴스를 생성하고 초기 환경 값을 설정"""
        self.sensor = DummySensor()
        self.env_values = {}
        self.running = True
        self.data_log = []  # 5분 평균 계산을 위한 데이터 저장 리스트

    def save_to_csv(self):
        """환경 값을 CSV 파일로 저장 (파일이 중복되지 않도록 자동 증가)"""
        file_index = 1

        while True:
            file_name = f'mars_live_data_{file_index}.csv'
            try:
                with open(file_name, 'r', encoding='utf-8'):
                    file_index += 1
            except FileNotFoundError:
                break

        with open(file_name, 'w', encoding='utf-8') as file:
            for key, value in self.env_values.items():
                file.write(f'{key}, {value}\n')

        print(f'환경 데이터가 {file_name} 파일로 저장되었습니다.')

    def get_sensor_data(self):
        """센서의 값을 가져와서 env_values에 저장하고 5초마다 JSON 형태로 출력"""
        start_time = time.time()
        
        while self.running:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            self.data_log.append(self.env_values.copy())
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

            if time.time() - start_time >= 300:
                self.print_avg_values()
                start_time = time.time()
                self.data_log.clear()
            
            time.sleep(5)
            
            user_input = input("종료하려면 1234를 입력하세요: ")
            if user_input.strip() == '1234':
                self.running = False
                print('System stopped….')
                self.save_to_csv()

    def print_avg_values(self):
        """5분 동안 수집된 데이터의 평균 값을 계산하여 출력"""
        if not self.data_log:
            return

        avg_values = {}
        num_entries = len(self.data_log)
        
        for key in self.data_log[0].keys():
            avg_values[key] = sum(entry[key] for entry in self.data_log) / num_entries
        
        print("5분 평균 환경 데이터:")
        print(json.dumps(avg_values, indent=4, ensure_ascii=False))

# RunComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
