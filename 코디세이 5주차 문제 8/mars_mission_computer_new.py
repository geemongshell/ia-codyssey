import random
import time
import threading
import platform
import psutil


class DummySensor:
    def __init__(self):
        self.env_values = {}

    def set_env(self):
        self.env_values = {
            'mars_base_internal_temperature': random.randint(18, 30),
            'mars_base_external_temperature': random.randint(0, 21),
            'mars_base_internal_humidity': random.randint(50, 60),
            'mars_base_external_illuminance': random.randint(500, 715),
            'mars_base_internal_Co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': random.randint(4, 7),
        }

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.sensor = DummySensor()
        self.env_values = {}
        self.running = True
        self.data_log = []
        self.settings = self.load_settings()

    def load_settings(self):
        settings = {'info': [], 'load': []}
        try:
            with open('setting.txt', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, values = line.strip().split('=')
                        settings[key.strip()] = [v.strip() for v in values.split(',')]
        except FileNotFoundError:
            print('[경고] setting.txt 파일이 존재하지 않아 기본 설정이 적용됩니다.')
        return settings

    def get_sensor_data(self):
        def sensor_loop():
            start_time = time.time()
            while self.running:
                self.sensor.set_env()
                self.env_values = self.sensor.get_env()
                self.data_log.append(self.env_values.copy())

                print(
                    '{{\n'
                    '    "mars_base_internal_temperature": {},\n'
                    '    "mars_base_external_temperature": {},\n'
                    '    "mars_base_internal_humidity": {},\n'
                    '    "mars_base_external_illuminance": {},\n'
                    '    "mars_base_internal_Co2": {},\n'
                    '    "mars_base_internal_oxygen": {}\n'
                    '}}'.format(
                        self.env_values['mars_base_internal_temperature'],
                        self.env_values['mars_base_external_temperature'],
                        self.env_values['mars_base_internal_humidity'],
                        self.env_values['mars_base_external_illuminance'],
                        self.env_values['mars_base_internal_Co2'],
                        self.env_values['mars_base_internal_oxygen']
                    )
                )

                if time.time() - start_time >= 300:
                    self.print_avg_values()
                    start_time = time.time()
                    self.data_log.clear()

                for _ in range(5):
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
                print('System stopped….\n')

                self.print_avg_values()
                self.get_mission_computer_info()
                self.get_mission_computer_load()

    def print_avg_values(self):
        if not self.data_log:
            print('No data to calculate average.')
            return

        avg_values = {}
        num_entries = len(self.data_log)

        for key in self.data_log[0].keys():
            avg_values[key] = sum(entry[key] for entry in self.data_log) / num_entries

        print('5분 평균 환경 데이터:')
        print(
            '{{\n'
            '    "mars_base_internal_temperature": {:.2f},\n'
            '    "mars_base_external_temperature": {:.2f},\n'
            '    "mars_base_internal_humidity": {:.2f},\n'
            '    "mars_base_external_illuminance": {:.2f},\n'
            '    "mars_base_internal_Co2": {:.2f},\n'
            '    "mars_base_internal_oxygen": {:.2f}\n'
            '}}'.format(
                avg_values['mars_base_internal_temperature'],
                avg_values['mars_base_external_temperature'],
                avg_values['mars_base_internal_humidity'],
                avg_values['mars_base_external_illuminance'],
                avg_values['mars_base_internal_Co2'],
                avg_values['mars_base_internal_oxygen']
            )
        )

    def get_mission_computer_info(self):
        selected = self.settings.get('info', [])

        info = {}
        if 'os' in selected:
            info['os'] = platform.system()
        if 'os_version' in selected:
            info['os_version'] = platform.version()
        if 'cpu_type' in selected:
            info['cpu_type'] = platform.processor()
        if 'cpu_cores' in selected:
            info['cpu_cores'] = psutil.cpu_count(logical=False)
        if 'memory_MB' in selected:
            info['memory_MB'] = round(psutil.virtual_memory().total / (1024 * 1024), 2)

        print('{')
        for i, (k, v) in enumerate(info.items()):
            comma = ',' if i < len(info) - 1 else ''
            print(f'    "{k}": "{v}"' if isinstance(v, str) else f'    "{k}": {v}', end=comma + '\n')
        print('}')

    def get_mission_computer_load(self):
        selected = self.settings.get('load', [])

        load = {}
        if 'cpu_usage_percent' in selected:
            load['cpu_usage_percent'] = psutil.cpu_percent(interval=1)
        if 'memory_usage_percent' in selected:
            load['memory_usage_percent'] = psutil.virtual_memory().percent

        print('{')
        for i, (k, v) in enumerate(load.items()):
            comma = ',' if i < len(load) - 1 else ''
            print(f'    "{k}": {v:.1f}', end=comma + '\n')
        print('}')


# 인스턴스 생성 및 실행
runComputer = MissionComputer()
runComputer.get_sensor_data()
