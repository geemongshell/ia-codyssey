import random
import time
import threading

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

    def get_sensor_data(self):
        """센서의 값을 가져와서 env_values에 저장하고 5초마다 JSON 형태로 출력"""
        def sensor_loop():
            start_time = time.time()
            while self.running:
                self.sensor.set_env()
                self.env_values = self.sensor.get_env()
                self.data_log.append(self.env_values.copy())

                # JSON 형식으로 출력 (import json 없이)
                print(
                    '{{\n'
                    '    "mars_base_internal_temperature": {},\n'
                    '    "mars_base_external_temperature": {},\n'
                    '    "mars_base_internal_humidity": {},\n'
                    '    "mars_base_external_illuminance": {},\n'
                    '    "mars_base_internal_Co2": {},\n'
                    '    "mars_base_internal_oxygen": {}\n'
                    '}}'.format(
                        self.env_values["mars_base_internal_temperature"],
                        self.env_values["mars_base_external_temperature"],
                        self.env_values["mars_base_internal_humidity"],
                        self.env_values["mars_base_external_illuminance"],
                        self.env_values["mars_base_internal_Co2"],
                        self.env_values["mars_base_internal_oxygen"]
                    )
                )

                if time.time() - start_time >= 300:
                    self.print_avg_values()
                    start_time = time.time()
                    self.data_log.clear()
                
                for _ in range(5):  # 5초 동안 입력 체크
                    if not self.running:
                        return
                    time.sleep(1)
        
        thread = threading.Thread(target=sensor_loop)
        thread.start()
        
        while self.running:
            user_input = input()
            if user_input.strip() == '1234':
                self.running = False
                thread.join()
                print('System stopped….')

    def print_avg_values(self):
        """5분 동안 수집된 데이터의 평균 값을 계산하여 출력"""
        if not self.data_log:
            return

        avg_values = {}
        num_entries = len(self.data_log)
        
        for key in self.data_log[0].keys():
            avg_values[key] = sum(entry[key] for entry in self.data_log) / num_entries
        
        print("5분 평균 환경 데이터:")
        print(
            '{{\n'
            '    "mars_base_internal_temperature": {:.2f},\n'
            '    "mars_base_external_temperature": {:.2f},\n'
            '    "mars_base_internal_humidity": {:.2f},\n'
            '    "mars_base_external_illuminance": {:.2f},\n'
            '    "mars_base_internal_Co2": {:.2f},\n'
            '    "mars_base_internal_oxygen": {:.2f}\n'
            '}}'.format(
                avg_values["mars_base_internal_temperature"],
                avg_values["mars_base_external_temperature"],
                avg_values["mars_base_internal_humidity"],
                avg_values["mars_base_external_illuminance"],
                avg_values["mars_base_internal_Co2"],
                avg_values["mars_base_internal_oxygen"]
            )
        )

# RunComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
