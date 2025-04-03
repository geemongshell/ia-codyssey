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

    def get_sensor_data(self):
        """센서 값을 5초마다 가져와 출력"""
        while True:
            # 센서 데이터 생성 및 출력
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
            
            # 5초 대기
            time.sleep(5)

# RunComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
