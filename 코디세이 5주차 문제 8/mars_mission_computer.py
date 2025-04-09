import random
import time
import threading
#추가된 라이부러링
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

                #종료되면 나오는 값
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
        system = platform.system()
        version = platform.version()
        processor = platform.processor()
        cores = psutil.cpu_count(logical=False)
        memory = round(psutil.virtual_memory().total / (1024 * 1024), 2)

        print('{{\n'
              '    "os": "{}",\n'
              '    "os_version": "{}",\n'
              '    "cpu_type": "{}",\n'
              '    "cpu_cores": {},\n'
              '    "memory_MB": {}\n'
              '}}'.format(system, version, processor, cores, memory))

    def get_mission_computer_load(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_usage = mem.percent

        print('{{\n'
              '    "cpu_usage_percent": {:.1f},\n'
              '    "memory_usage_percent": {:.1f}\n'
              '}}'.format(cpu_usage, mem_usage))


# 인스턴스 생성 및 실행
runComputer = MissionComputer()
runComputer.get_sensor_data()
